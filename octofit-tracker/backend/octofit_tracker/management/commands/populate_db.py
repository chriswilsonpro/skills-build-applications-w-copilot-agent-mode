
from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.db import connection
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Dropping old collections directly in MongoDB...'))
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        for coll in ['activity', 'workout', 'leaderboard', 'user', 'team']:
            db[coll].drop()
        client.close()

        self.stdout.write(self.style.SUCCESS('Creating teams...'))
        marvel = Team.objects.create(name='Marvel', description='Marvel superheroes')
        dc = Team.objects.create(name='DC', description='DC superheroes')

        self.stdout.write(self.style.SUCCESS('Creating users...'))
        users = [
            User.objects.create(name='Spider-Man', email='spiderman@marvel.com', team=marvel),
            User.objects.create(name='Iron Man', email='ironman@marvel.com', team=marvel),
            User.objects.create(name='Wonder Woman', email='wonderwoman@dc.com', team=dc),
            User.objects.create(name='Batman', email='batman@dc.com', team=dc),
        ]

        self.stdout.write(self.style.SUCCESS('Creating activities...'))
        Activity.objects.create(user=users[0], type='Web Swinging', duration=60, date='2023-01-01')
        Activity.objects.create(user=users[1], type='Suit Training', duration=45, date='2023-01-02')
        Activity.objects.create(user=users[2], type='Lasso Practice', duration=30, date='2023-01-03')
        Activity.objects.create(user=users[3], type='Martial Arts', duration=50, date='2023-01-04')

        self.stdout.write(self.style.SUCCESS('Creating workouts...'))
        w1 = Workout.objects.create(name='Super Strength', description='Strength workout for heroes')
        w2 = Workout.objects.create(name='Agility Drills', description='Agility workout for heroes')
        w1.suggested_for.set(users)
        w2.suggested_for.set(users)

        self.stdout.write(self.style.SUCCESS('Creating leaderboards...'))
        Leaderboard.objects.create(team=marvel, points=200)
        Leaderboard.objects.create(team=dc, points=180)

        self.stdout.write(self.style.SUCCESS('Ensuring unique index on user email...'))
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        db.user.create_index([('email', 1)], unique=True)
        client.close()

        self.stdout.write(self.style.SUCCESS('Database populated with test data!'))
