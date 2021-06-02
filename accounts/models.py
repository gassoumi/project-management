from django.db import models
from django.contrib.auth.models import User


# https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#extending-the-existing-user-model
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='userProfile', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    # only is_manager can create or edir project or sprint or task
    is_manager = models.BooleanField(default=False)

    def __str__(self):
        return "User Information"
