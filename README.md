# HabitHero - Build Better Habits Every Day 🚀

<div align="center">

![HabitHero Banner](https://via.placeholder.com/800x200/667eea/ffffff?text=HabitHero+-+Build+Better+Habits)

**Transform your life one habit at a time with our intuitive habit-tracking platform**

[![React](https://img.shields.io/badge/React-18.2.0-61dafb?logo=react)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-black?logo=flask)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3.40-lightgrey?logo=sqlite)](https://sqlite.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-7952B3?logo=bootstrap)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

[Features](#-features) • [Demo](#-demo) • [Quick Start](#-quick-start) • [API](#-api-documentation) • [Contributing](#-contributing)

</div>

## 📖 Overview

HabitHero is a full-stack web application designed to help users build and maintain positive habits through consistent tracking, motivational insights, and data-driven analytics. Whether you're starting a fitness routine, learning a new skill, or improving daily productivity, HabitHero provides the tools you need to succeed.

## ✨ Features

### 🔐 **Authentication & Security**
- User registration and login system
- Session-based authentication
- Secure password hashing with Werkzeug
- Protected routes and API endpoints

### 📊 **Habit Management**
- **Create Habits**: Add custom habits with names, categories, and frequencies
- **Flexible Tracking**: Support for daily and weekly habit frequencies
- **Categories**: Organize by Health, Work, Learning, Fitness, Mental Wellness, Productivity
- **Progress Visualization**: Real-time progress indicators and streaks
- **Quick Actions**: One-click habit completion with notes

### 📈 **Advanced Analytics**
- **Success Rate Dashboard**: Overall completion percentage tracking
- **Streak Counter**: Consecutive days of habit maintenance
- **Best Day Analysis**: Identify most productive days of the week
- **7-Day Progress Charts**: Visual success rate trends
- **Calendar Integration**: Monthly habit completion overview
- **Category Insights**: Performance breakdown by habit type

### 🎯 **Motivation & Engagement**
- **AI-Powered Quotes**: Personalized motivational messages based on progress
- **Achievement System**: Visual rewards for maintaining streaks
- **Progress Celebrations**: Success popups with streak updates
- **Daily Reminders**: Visual indicators for pending habits

### 🎨 **User Experience**
- **Responsive Design**: Seamless experience across desktop and mobile
- **Modern UI**: Clean, intuitive interface with Bootstrap 5
- **Real-time Updates**: Instant feedback on all interactions
- **Accessibility**: WCAG compliant design patterns

## 🛠️ Tech Stack

### Frontend
- **React 18** - Modern React with hooks and functional components
- **React Router DOM** - Client-side routing and navigation
- **Bootstrap 5** - Responsive UI framework and components
- **Bootstrap Icons** - Comprehensive icon library
- **CSS3** - Custom animations and responsive design

### Backend
- **Flask** - Lightweight Python web framework
- **Flask-SQLAlchemy** - Database ORM and management
- **Flask-CORS** - Cross-origin resource sharing
- **Werkzeug** - Security utilities and password hashing

### Database
- **SQLite** - Lightweight, file-based database
- **SQLAlchemy** - Database migrations and query management

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/habithero.git
cd habithero
```

2. **Backend Setup**
```bash
cd HabitHero-BackendAPI

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Unix/MacOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start backend server
python app.py
```
Backend server runs on `http://localhost:5000`

3. **Frontend Setup**
```bash
cd ../HabitHero-Frontend

# Install dependencies
npm install

# Start development server
npm start
```
Frontend runs on `http://localhost:3000`

### Environment Configuration

Create a `.env` file in the backend directory:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///habithero.db
SQLALCHEMY_TRACK_MODIFICATIONS=False
```

## 📁 Project Structure

```
habithero/
├── HabitHero-BackendAPI/
│   ├── controllers/          # Business logic
│   │   ├── authController.py
│   │   └── habitController.py
│   ├── models/              # Database models
│   │   ├── __init__.py
│   │   ├── userModel.py
│   │   └── habitModel.py
│   ├── routes/              # API routes
│   │   ├── authRoutes.py
│   │   └── habitRoutes.py
│   ├── instance/            # Database files
│   ├── app.py              # Flask application
│   ├── config.py           # Configuration
│   └── requirements.txt    # Python dependencies
└── HabitHero-Frontend/
    ├── public/             # Static assets
    ├── src/
    │   ├── components/     # React components
    │   │   ├── AddHabit.jsx
    │   │   ├── Analytics.jsx
    │   │   ├── Dashboard.jsx
    │   │   ├── Login.jsx
    │   │   ├── Register.jsx
    │   │   └── TodaysHabits.jsx
    │   ├── App.jsx         # Main app component
    │   ├── App.css         # Global styles
    │   └── main.jsx        # React entry point
    ├── package.json        # Node dependencies
    └── README.md
```

## 📚 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| `POST` | `/api/auth/register` | User registration | `{name, email, password, confirmPassword}` |
| `POST` | `/api/auth/login` | User login | `{email, password}` |
| `POST` | `/api/auth/logout` | User logout | - |
| `GET` | `/api/auth/me` | Get current user | - |

### Habit Endpoints

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| `POST` | `/api/habits` | Create new habit | `{name, frequency, category, start_date, target_duration, note}` |
| `GET` | `/api/habits` | Get all user habits | - |
| `GET` | `/api/habits/today` | Get today's habits | - |
| `POST` | `/api/habits/mark-done` | Mark habit as completed | `{habit_id, notes}` |
| `DELETE` | `/api/habits` | Delete habit | `habit_id` (query param) |
| `GET` | `/api/habits/analytics` | Get user analytics | - |
| `GET` | `/api/habits/calendar` | Get calendar data | - |
| `GET` | `/api/habits/motivational-quote` | Get motivational quote | - |

### Example API Usage

```javascript
// Create a new habit
const response = await fetch('/api/habits', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  credentials: 'include',
  body: JSON.stringify({
    name: 'Morning Meditation',
    frequency: 'daily',
    category: 'Mental Wellness',
    start_date: '2024-01-15',
    target_duration: 30,
    note: 'Start day with clarity'
  })
});
```

## 🎯 Usage Guide

### Getting Started
1. **Register an Account**: Create your HabitHero account
2. **Add Your First Habit**: Use the "Add Habit" feature to create habits
3. **Set Categories**: Organize habits by relevant categories
4. **Track Daily**: Mark habits as completed each day

### Best Practices
- Start with 3-5 manageable habits
- Use specific, measurable habit names
- Set realistic target durations
- Review analytics weekly to track progress
- Use the motivational quotes for daily inspiration

### Mobile Usage
The application is fully responsive and works seamlessly on mobile devices, allowing you to track habits on-the-go.

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -m 'Add amazing feature'`
5. Push to the branch: `git push origin feature/amazing-feature`
6. Open a Pull Request

### Contribution Guidelines
- Follow the existing code style
- Add comments for complex logic
- Update documentation as needed
- Test your changes across different devices
- Ensure all endpoints return appropriate status codes


<img width="1910" height="1020" alt="Screenshot 2025-11-15 201416" src="https://github.com/user-attachments/assets/ef05f397-cbab-4abc-8653-c2b654b94f36" />
<img width="1919" height="1079" alt="Screenshot 2025-11-15 201450" src="https://github.com/user-attachments/assets/e166b197-80de-417a-91f7-c45715d4367a" />
<img width="1919" height="1079" alt="Screenshot 2025-11-15 201507" src="https://github.com/user-attachments/assets/7a9bf07c-d63c-43ba-9917-9ab1d5638a38" />


<img width="1919" height="1079" alt="Screenshot 2025-11-15 201528" src="https://github.com/user-attachments/assets/3fefbc5e-83f6-4a18-8693-73f309e370c8" />
<img width="1919" height="1079" alt="Screenshot 2025-11-15 201546" src="https://github.com/user-attachments/assets/719345c7-5e35-4b48-be69-b6446d0a526a" />

**Build better habits, build a better you with HabitHero** 🌟

</div>
