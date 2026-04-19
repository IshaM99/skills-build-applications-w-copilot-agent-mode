from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Leaderboard.objects.all().delete()
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        Team.objects.all().delete()
        User.objects.all().delete()

        # Create users (super heroes)
        marvel_heroes = [
            {'username': 'ironman', 'email': 'ironman@marvel.com'},
            {'username': 'captainamerica', 'email': 'cap@marvel.com'},
            {'username': 'spiderman', 'email': 'spiderman@marvel.com'},
        ]
        dc_heroes = [
            {'username': 'batman', 'email': 'batman@dc.com'},
            {'username': 'superman', 'email': 'superman@dc.com'},
            {'username': 'wonderwoman', 'email': 'wonderwoman@dc.com'},
        ]
        marvel_users = [User.objects.create_user(**hero) for hero in marvel_heroes]
        dc_users = [User.objects.create_user(**hero) for hero in dc_heroes]

        # Create teams
        marvel_team = Team.objects.create(name='Marvel')
        marvel_team.members.set(marvel_users)
        dc_team = Team.objects.create(name='DC')
        dc_team.members.set(dc_users)

        # Create workouts
        workout1 = Workout.objects.create(name='Super Strength', description='Strength training for heroes')
        workout2 = Workout.objects.create(name='Agility Training', description='Agility and speed drills')
        workout1.suggested_for.set(marvel_users + dc_users)
        workout2.suggested_for.set(marvel_users + dc_users)

        # Create activities
        for user in marvel_users + dc_users:
            Activity.objects.create(
                user=user,
                activity_type='Training',
                duration=60,
                calories_burned=500,
                date=timezone.now().date()
            )

        # Create leaderboard
        Leaderboard.objects.create(team=marvel_team, score=100)
        Leaderboard.objects.create(team=dc_team, score=90)

        self.stdout.write(self.style.SUCCESS('Test data populated successfully.'))
