from flask_sqlalchemy import SQLAlchemy

# Create db instance
db = SQLAlchemy()

# Import models after db is created
from .userModel import User
from .habitModel import Habit, HabitCheckin