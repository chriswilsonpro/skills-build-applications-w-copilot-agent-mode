from django.db import models



from django.utils.crypto import get_random_string

def random_id():
    return get_random_string(24)

class Team(models.Model):
    id = models.CharField(primary_key=True, max_length=24, editable=False, default=random_id)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class User(models.Model):
    id = models.CharField(primary_key=True, max_length=24, editable=False, default=random_id)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    team = models.ForeignKey(Team, related_name='members', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Activity(models.Model):
    id = models.CharField(primary_key=True, max_length=24, editable=False, default=random_id)
    user = models.ForeignKey(User, related_name='activities', on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    duration = models.PositiveIntegerField(help_text='Duration in minutes')
    date = models.DateField()

    def __str__(self):
        return f"{self.user.name} - {self.type} on {self.date}"

class Workout(models.Model):
    id = models.CharField(primary_key=True, max_length=24, editable=False, default=random_id)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    suggested_for = models.ManyToManyField(User, related_name='suggested_workouts', blank=True)

    def __str__(self):
        return self.name

class Leaderboard(models.Model):
    id = models.CharField(primary_key=True, max_length=24, editable=False, default=random_id)
    team = models.OneToOneField(Team, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.team.name} - {self.points} points"
