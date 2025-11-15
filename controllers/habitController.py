from flask import jsonify, request, session
from models.userModel import db, User
from models.habitModel import Habit, HabitCheckin
import datetime
import random

# Helper functions
def calculate_streak(habit_id):
    try:
        checkins = HabitCheckin.query.filter_by(
            habit_id=habit_id, 
            status='completed'
        ).order_by(HabitCheckin.checkin_date.desc()).all()
        
        if not checkins:
            return 0
        
        streak = 0
        current_date = datetime.datetime.now().date()
        
        for checkin in checkins:
            checkin_date = checkin.checkin_date.date()
            
            if (current_date - checkin_date).days == streak:
                streak += 1
            else:
                break
        
        return streak
    except Exception as e:
        print(f"Calculate streak error: {str(e)}")
        return 0

def calculate_best_day(habit_ids):
    try:
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        checkins = HabitCheckin.query.filter(
            HabitCheckin.habit_id.in_(habit_ids),
            HabitCheckin.status == 'completed'
        ).all()
        
        if not checkins:
            return 'No data yet'
        
        day_counts = {i: 0 for i in range(7)}
        for checkin in checkins:
            day_of_week = checkin.checkin_date.weekday()
            day_counts[day_of_week] += 1
        
        best_day_index = max(day_counts, key=day_counts.get)
        return day_names[best_day_index]
        
    except Exception as e:
        print(f"Best day calculation error: {str(e)}")
        return 'Unknown'

def generate_motivational_quote(success_rate, total_habits):
    quotes_by_category = {
        'high_performance': [
            {
                "text": "Your consistency is inspiring! Keep building those powerful habits that shape your destiny.",
                "author": "HabitHero AI",
                "category": "High Performance"
            },
            {
                "text": "Excellence is not a single act, but a habit. You are what you repeatedly do!",
                "author": "Aristotle",
                "category": "Consistency"
            }
        ],
        'medium_performance': [
            {
                "text": "Progress, not perfection. Every small step counts on your journey to greatness.",
                "author": "HabitHero AI", 
                "category": "Progress"
            },
            {
                "text": "The journey of a thousand miles begins with a single step. You're on your way!",
                "author": "Lao Tzu",
                "category": "Journey"
            }
        ],
        'low_performance': [
            {
                "text": "Every master was once a beginner. Your commitment to starting is what truly matters.",
                "author": "HabitHero AI",
                "category": "Encouragement"
            },
            {
                "text": "Don't let yesterday take up too much of today. Every day is a new beginning!",
                "author": "Will Rogers",
                "category": "Fresh Start"
            }
        ],
        'new_user': [
            {
                "text": "The first step towards getting somewhere is to decide you're not going to stay where you are.",
                "author": "John Pierpont Morgan",
                "category": "Beginning"
            },
            {
                "text": "Your future self will thank you for the habits you start building today.",
                "author": "HabitHero AI",
                "category": "Future Self"
            }
        ]
    }
    
    if total_habits == 0:
        category = 'new_user'
    elif success_rate >= 80:
        category = 'high_performance'
    elif success_rate >= 50:
        category = 'medium_performance'
    else:
        category = 'low_performance'
    
    return random.choice(quotes_by_category[category])

def get_current_user_id():
    user_id = session.get('user_id')
    if not user_id:
        return None
    return user_id

# Habit Routes
def create_habit():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        
        required_fields = ['name', 'frequency', 'category', 'start_date', 'target_duration']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({'success': False, 'error': f'Missing fields: {", ".join(missing_fields)}'}), 400
        
        if data['frequency'] not in ['daily', 'weekly']:
            return jsonify({'success': False, 'error': 'Frequency must be daily or weekly'}), 400
        
        valid_categories = ['health', 'work', 'learning', 'Lifestyle', 'Fitness', 'Mental Wellness', 'Productivity']
        if data['category'] not in valid_categories:
            return jsonify({'success': False, 'error': 'Invalid category'}), 400
        
        try:
            start_date = datetime.datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
        except:
            return jsonify({'success': False, 'error': 'Invalid start date format'}), 400
        
        new_habit = Habit(
            user_id=user_id,
            name=data['name'].strip(),
            frequency=data['frequency'],
            category=data['category'],
            start_date=start_date,
            target_duration=data['target_duration'],
            note=data.get('note', '').strip()
        )
        
        db.session.add(new_habit)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Habit created successfully',
            'habit': new_habit.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Create habit error: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to create habit'}), 500

def get_user_habits():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        habits = Habit.query.filter_by(user_id=user_id).all()
        return jsonify({
            'success': True,
            'habits': [habit.to_dict() for habit in habits]
        }), 200
    except Exception as e:
        print(f"Get habits error: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to fetch habits'}), 500

def get_today_habits():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        today = datetime.datetime.now().date()
        habits = Habit.query.filter_by(user_id=user_id).all()
        
        today_habits = []
        for habit in habits:
            if habit.frequency == 'daily':
                if habit.start_date.date() <= today:
                    today_habits.append(habit)
            elif habit.frequency == 'weekly':
                if habit.start_date.date() <= today and habit.start_date.weekday() == today.weekday():
                    today_habits.append(habit)
        
        result_habits = []
        for habit in today_habits:
            habit_dict = habit.to_dict()
            
            today_checkin = HabitCheckin.query.filter_by(
                habit_id=habit.id,
                checkin_date=datetime.datetime.combine(today, datetime.datetime.min.time())
            ).first()
            
            habit_dict['checked_in_today'] = today_checkin.status if today_checkin else 'pending'
            habit_dict['today_checkin_id'] = today_checkin.id if today_checkin else None
            habit_dict['current_streak'] = calculate_streak(habit.id)
            
            result_habits.append(habit_dict)
        
        return jsonify({
            'success': True,
            'habits': result_habits
        }), 200
        
    except Exception as e:
        print(f"Get today habits error: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to fetch today\'s habits'}), 500

def mark_habit_done():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        habit_id = data.get('habit_id')
        
        if not habit_id:
            return jsonify({'success': False, 'error': 'Habit ID is required'}), 400
        
        habit = Habit.query.filter_by(id=habit_id, user_id=user_id).first()
        if not habit:
            return jsonify({'success': False, 'error': 'Habit not found'}), 404
        
        today = datetime.datetime.now().date()
        
        existing_checkin = HabitCheckin.query.filter_by(
            habit_id=habit_id,
            checkin_date=datetime.datetime.combine(today, datetime.datetime.min.time())
        ).first()
        
        if existing_checkin:
            return jsonify({'success': False, 'error': 'Habit already checked in today'}), 400
        
        new_checkin = HabitCheckin(
            habit_id=habit_id,
            checkin_date=datetime.datetime.combine(today, datetime.datetime.min.time()),
            status='completed',
            notes=data.get('notes', '')
        )
        
        db.session.add(new_checkin)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Habit marked as done',
            'checkin': new_checkin.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Mark habit done error: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to mark habit as done'}), 500

def delete_habit():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        habit_id = request.args.get('habit_id')
        
        if not habit_id:
            return jsonify({'success': False, 'error': 'Habit ID is required'}), 400
        
        habit = Habit.query.filter_by(id=habit_id, user_id=user_id).first()
        if not habit:
            return jsonify({'success': False, 'error': 'Habit not found'}), 404
        
        db.session.delete(habit)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Habit deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Delete habit error: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to delete habit'}), 500

def get_user_analytics():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        habits = Habit.query.filter_by(user_id=user_id).all()
        habit_ids = [habit.id for habit in habits]
        
        if not habit_ids:
            return jsonify({
                'success': True,
                'analytics': {
                    'success_rate': 0,
                    'total_habits': 0,
                    'completed_checkins': 0,
                    'current_streak': 0,
                    'best_day': 'No data yet'
                }
            }), 200
        
        total_checkins = HabitCheckin.query.filter(HabitCheckin.habit_id.in_(habit_ids)).count()
        completed_checkins = HabitCheckin.query.filter(
            HabitCheckin.habit_id.in_(habit_ids),
            HabitCheckin.status == 'completed'
        ).count()
        
        success_rate = (completed_checkins / total_checkins * 100) if total_checkins > 0 else 0
        
        best_day = calculate_best_day(habit_ids)
        current_streak = max([calculate_streak(habit.id) for habit in habits]) if habits else 0
        
        return jsonify({
            'success': True,
            'analytics': {
                'success_rate': round(success_rate, 1),
                'total_habits': len(habits),
                'completed_checkins': completed_checkins,
                'current_streak': current_streak,
                'best_day': best_day
            }
        }), 200
        
    except Exception as e:
        print(f"Analytics error: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to fetch analytics'}), 500

def get_calendar_data():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        habits = Habit.query.filter_by(user_id=user_id).all()
        habit_ids = [habit.id for habit in habits]
        
        if not habit_ids:
            return jsonify({'success': True, 'calendar_data': []}), 200
        
        thirty_days_ago = datetime.datetime.now() - datetime.timedelta(days=30)
        checkins = HabitCheckin.query.filter(
            HabitCheckin.habit_id.in_(habit_ids),
            HabitCheckin.status == 'completed',
            HabitCheckin.checkin_date >= thirty_days_ago
        ).all()
        
        calendar_data = []
        for checkin in checkins:
            calendar_data.append({
                'date': checkin.checkin_date.strftime('%Y-%m-%d'),
                'habit_name': checkin.habit.name,
                'count': 1
            })
        
        return jsonify({
            'success': True,
            'calendar_data': calendar_data
        }), 200
        
    except Exception as e:
        print(f"Calendar data error: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to fetch calendar data'}), 500

def get_motivational_quote():
    user_id = get_current_user_id()
    if not user_id:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        habits = Habit.query.filter_by(user_id=user_id).all()
        habit_ids = [habit.id for habit in habits]
        
        seven_days_ago = datetime.datetime.now() - datetime.timedelta(days=7)
        recent_checkins = HabitCheckin.query.filter(
            HabitCheckin.habit_id.in_(habit_ids),
            HabitCheckin.checkin_date >= seven_days_ago,
            HabitCheckin.status == 'completed'
        ).count()
        
        total_possible = len(habits) * 7
        recent_success_rate = (recent_checkins / total_possible * 100) if total_possible > 0 else 0
        
        quote = generate_motivational_quote(recent_success_rate, len(habits))
        
        return jsonify({
            'success': True,
            'quote': quote['text'],
            'author': quote['author'],
            'category': quote['category']
        }), 200
        
    except Exception as e:
        print(f"AI quote error: {str(e)}")
        fallback_quotes = [
            {
                "text": "We are what we repeatedly do. Excellence, then, is not an act, but a habit.",
                "author": "Will Durant",
                "category": "Excellence"
            },
            {
                "text": "Small daily improvements are the key to staggering long-term results.",
                "author": "Robin Sharma", 
                "category": "Improvement"
            }
        ]
        quote = random.choice(fallback_quotes)
        return jsonify({
            'success': True,
            'quote': quote['text'],
            'author': quote['author'],
            'category': quote['category']
        }), 200
@token_required
def get_completed_today_habits(current_user):
    try:
        today = datetime.datetime.now().date()
        
        # Get habits that were completed today
        completed_checkins = HabitCheckin.query.filter(
            HabitCheckin.checkin_date >= datetime.datetime.combine(today, datetime.datetime.min.time()),
            HabitCheckin.checkin_date < datetime.datetime.combine(today + datetime.timedelta(days=1), datetime.datetime.min.time()),
            HabitCheckin.status == 'completed'
        ).all()
        
        completed_habits = [checkin.habit for checkin in completed_checkins if checkin.habit.user_id == current_user.id]
        
        return jsonify({
            'success': True,
            'habits': [habit.to_dict() for habit in completed_habits]
        }), 200
        
    except Exception as e:
        print(f"Get completed habits error: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to fetch completed habits'}), 500

@token_required
def get_failed_today_habits(current_user):
    try:
        today = datetime.datetime.now().date()
        habits = Habit.query.filter_by(user_id=current_user.id).all()
        
        failed_habits = []
        for habit in habits:
            # Check if habit should be done today
            should_be_done = False
            if habit.frequency == 'daily':
                should_be_done = habit.start_date.date() <= today
            elif habit.frequency == 'weekly':
                should_be_done = (habit.start_date.date() <= today and 
                                habit.start_date.weekday() == today.weekday())
            
            if should_be_done:
                # Check if not completed today
                today_checkin = HabitCheckin.query.filter_by(
                    habit_id=habit.id,
                    checkin_date=datetime.datetime.combine(today, datetime.datetime.min.time())
                ).first()
                
                if not today_checkin or today_checkin.status != 'completed':
                    habit_dict = habit.to_dict()
                    habit_dict['current_streak'] = calculate_streak(habit.id)
                    failed_habits.append(habit_dict)
        
        return jsonify({
            'success': True,
            'habits': failed_habits
        }), 200
        
    except Exception as e:
        print(f"Get failed habits error: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to fetch failed habits'}), 500

@token_required
def get_habits_by_category(current_user):
    try:
        category = request.args.get('category')
        if category:
            habits = Habit.query.filter_by(user_id=current_user.id, category=category).all()
        else:
            habits = Habit.query.filter_by(user_id=current_user.id).all()
        
        return jsonify({
            'success': True,
            'habits': [habit.to_dict() for habit in habits]
        }), 200
        
    except Exception as e:
        print(f"Get habits by category error: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to fetch habits'}), 500

@token_required
def get_daily_success_data(current_user):
    try:
        # Get last 7 days data
        end_date = datetime.datetime.now().date()
        start_date = end_date - datetime.timedelta(days=6)
        
        daily_data = []
        current_date = start_date
        
        while current_date <= end_date:
            # Get total habits that should be done on this day
            habits = Habit.query.filter_by(user_id=current_user.id).all()
            total_possible = 0
            completed = 0
            
            for habit in habits:
                if habit.frequency == 'daily':
                    if habit.start_date.date() <= current_date:
                        total_possible += 1
                elif habit.frequency == 'weekly':
                    if habit.start_date.date() <= current_date and habit.start_date.weekday() == current_date.weekday():
                        total_possible += 1
            
            # Get completed checkins for this day
            if total_possible > 0:
                checkins = HabitCheckin.query.filter(
                    HabitCheckin.habit_id.in_([h.id for h in habits]),
                    HabitCheckin.checkin_date >= datetime.datetime.combine(current_date, datetime.datetime.min.time()),
                    HabitCheckin.checkin_date < datetime.datetime.combine(current_date + datetime.timedelta(days=1), datetime.datetime.min.time()),
                    HabitCheckin.status == 'completed'
                ).count()
                completed = checkins
            
            success_rate = (completed / total_possible * 100) if total_possible > 0 else 0
            
            daily_data.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'day': current_date.strftime('%a'),
                'success_rate': round(success_rate, 1),
                'completed': completed,
                'total': total_possible
            })
            
            current_date += datetime.timedelta(days=1)
        
        return jsonify({
            'success': True,
            'data': daily_data
        }), 200
        
    except Exception as e:
        print(f"Get daily success data error: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to fetch daily success data'}), 500