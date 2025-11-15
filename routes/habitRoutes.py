from flask import Blueprint
from controllers.habitController import (
    create_habit, get_user_habits, get_today_habits, mark_habit_done, 
    delete_habit, get_user_analytics, get_calendar_data, get_motivational_quote
)

habit_bp = Blueprint('habits', __name__)

# Habit routes
habit_bp.route('', methods=['POST'])(create_habit)
habit_bp.route('', methods=['GET'])(get_user_habits)
habit_bp.route('/today', methods=['GET'])(get_today_habits)
habit_bp.route('/mark-done', methods=['POST'])(mark_habit_done)
habit_bp.route('', methods=['DELETE'])(delete_habit)
# Add these to existing routes
habit_bp.route('/completed-today', methods=['GET'])(get_completed_today_habits)
habit_bp.route('/failed-today', methods=['GET'])(get_failed_today_habits)
habit_bp.route('/by-category', methods=['GET'])(get_habits_by_category)
habit_bp.route('/daily-success', methods=['GET'])(get_daily_success_data)

# Analytics routes
habit_bp.route('/analytics', methods=['GET'])(get_user_analytics)
habit_bp.route('/calendar', methods=['GET'])(get_calendar_data)

# AI routes
habit_bp.route('/motivational-quote', methods=['GET'])(get_motivational_quote)