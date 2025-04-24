from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from pets.choices import FUR_CHOICES,DOG_BREEDS,CAT_BREEDS,SIZE_CHOICES,GENDER_CHOICES,SPECIES_CHOICES
from django.db import models
from django.apps import apps
    

class CustomUser(AbstractUser):
    # 3 types of users
    USER_TYPE_CHOICES = [
        ('simple', 'Simple'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]

    
    # 4 types of foster badge statuses
    FOSTERER_STATUS_CHOICES = [
        ('none', 'None'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
    ]


    user_type = models.CharField(max_length=10,choices=USER_TYPE_CHOICES,default='simple')
    fosterer_status = models.CharField(max_length=10,choices=FOSTERER_STATUS_CHOICES,default='none')
    profile_photo = models.ImageField(upload_to='profile_photos/',  default='pets/images/userprofile.png') 

    def __str__(self):
        return self.username



#for suggestions of ideal pet
class IdealPetProfile(models.Model):
    gender=models.CharField(max_length=50,blank=True, choices=GENDER_CHOICES, null=True)
    size=models.CharField(max_length=50,blank=True, choices=SIZE_CHOICES, null=True)
    species = models.CharField(max_length=10, choices=SPECIES_CHOICES, blank=True, null=True)
    dog_breed = models.CharField(max_length=50, choices=DOG_BREEDS, blank=True, null=True)
    cat_breed = models.CharField(max_length=50, choices=CAT_BREEDS, blank=True, null=True)
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name='ideal_pet_profile')
    min_age = models.IntegerField(blank=True, null=True)
    max_age = models.IntegerField(blank=True, null=True)
    fur = models.CharField(max_length=10, choices=FUR_CHOICES, blank=True, null=True)

    character_traits = models.ManyToManyField('pets.CharacterTrait',blank=True)
    allergies = models.ManyToManyField('pets.Allergy',blank=True)
    disabilities = models.ManyToManyField('pets.Disability',blank=True)


    def clean(self):
        if self.species == 'Dog':
            if self.cat_breed:
                raise ValidationError("Cat breed should not be filled when species is Dog.")

        elif self.species == 'Cat':
            if self.dog_breed:
                raise ValidationError("Dog breed should not be filled when species is Cat.")

        if not self.species:
            if self.dog_breed or self.cat_breed:
                raise ValidationError("Cannot select breed without selecting species.")

    def save(self, *args, **kwargs):
       
        if self.species and self.species.lower() == 'dog':
            self.cat_breed = None
        elif self.species and self.species.lower() == 'cat':
            self.dog_breed = None
        else:
            self.cat_breed = None
            self.dog_breed = None

            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s Ideal Pet"
        



class FosteringApplication(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150, blank=False, null=False, default='n/a')
    last_name = models.CharField(max_length=150, blank=False, null=False, default='n/a')
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    proof_of_identity = models.FileField(upload_to='fostering/identity/')
    proof_of_residence = models.FileField(upload_to='fostering/residence/')
    prior_experience = models.TextField(blank=True)

    submitted_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} -  Application"



