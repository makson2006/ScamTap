from celery import shared_task
from django.contrib.auth.models import User

@shared_task
def add_point_every_second(user_id):
    try:
        user = User.objects.get(id=user_id)
        profile = user.profile
        if profile.miners > 0:
            profile.points += 10
            profile.save()
            print(f"Added 10 points to {user.username}. Total points: {profile.points}")
    except User.DoesNotExist:
        print(f"User with id {user_id} does not exist.")
