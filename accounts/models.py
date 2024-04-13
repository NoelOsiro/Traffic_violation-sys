# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    A custom user model for the Traffic Violation System.

    Attributes:
        ROLES (tuple): Choices for the user roles.
        role (str): The role of the user.
        profile_picture (ImageField): The profile picture of the user.
        phone_number (str): The phone number of the user.
        address (str): The address of the user.
        emergency_contact (str): The emergency contact of the user.
        license_plate_number (str): The license plate number of the user.
    """

    ROLES = (
        ('user', 'User'),
        ('administrator', 'Administrator'),
        ('moderator', 'Moderator'),
    )
    
    role = models.CharField(max_length=20, choices=ROLES, default='user')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    license_plate_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if self.role not in dict(self.ROLES).keys():
            raise ValueError('Invalid role specified.')
        super().save(*args, **kwargs)
