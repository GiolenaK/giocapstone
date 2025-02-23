from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # 3 types of users
    USER_TYPE_CHOICES = [
        ('simple', 'Simple'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]

    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='simple'
    )
    
    # 4 types of foster badge statuses
    FOSTERER_STATUS_CHOICES = [
        ('none', 'None'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
    ]

    fosterer_status = models.CharField(
        max_length=10,
        choices=FOSTERER_STATUS_CHOICES,
        default='none'
    )

    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)  # TO DO : ADD RANDOM IMAGE GEN FOR THIS

    def __str__(self):
        return self.username
