# accounts/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Position(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # Add this field:
    can_create_job_cards = models.BooleanField(
        default=False,
        help_text="Allow users with this position to create new job cards."
    )

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_id_no = models.CharField(max_length=50, blank=True, null=True)
    initial = models.CharField(max_length=10, blank=True, null=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, blank=True, null=True)
    ate_staff = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username

# Signal to create/update UserProfile when a User is created/updated
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    # Ensure UserProfile exists before trying to save it
    profile, created_profile = UserProfile.objects.get_or_create(user=instance)
    if not created_profile: # If profile already existed, save it
        profile.save()
