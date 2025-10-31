from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

from pymongo import MongoClient

# Sample data for users, teams, activities, leaderboard, workouts
USERS = [
    {"name": "Superman", "email": "superman@dc.com", "team": "dc"},
    {"name": "Batman", "email": "batman@dc.com", "team": "dc"},
    {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "dc"},
    {"name": "Iron Man", "email": "ironman@marvel.com", "team": "marvel"},
    {"name": "Captain America", "email": "cap@marvel.com", "team": "marvel"},
    {"name": "Black Widow", "email": "widow@marvel.com", "team": "marvel"},
]

TEAMS = [
    {"name": "marvel", "members": ["ironman@marvel.com", "cap@marvel.com", "widow@marvel.com"]},
    {"name": "dc", "members": ["superman@dc.com", "batman@dc.com", "wonderwoman@dc.com"]},
]

ACTIVITIES = [
    {"user_email": "superman@dc.com", "activity": "Flying", "duration": 60},
    {"user_email": "ironman@marvel.com", "activity": "Flight Training", "duration": 45},
]

LEADERBOARD = [
    {"team": "marvel", "points": 300},
    {"team": "dc", "points": 250},
]

WORKOUTS = [
    {"name": "Super Strength", "description": "Heavy lifting and strength training."},
    {"name": "Agility", "description": "Speed and agility drills."},
]

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Insert test data
        db.users.insert_many(USERS)
        db.teams.insert_many(TEAMS)
        db.activities.insert_many(ACTIVITIES)
        db.leaderboard.insert_many(LEADERBOARD)
        db.workouts.insert_many(WORKOUTS)

        # Ensure unique index on email
        db.users.create_index([("email", 1)], unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
