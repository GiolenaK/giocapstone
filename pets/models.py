from django.core.exceptions import ValidationError
from django.db import models
import random
from django.contrib.auth import get_user_model
from .choices import FUR_CHOICES,DOG_BREEDS,CAT_BREEDS,SIZE_CHOICES,GENDER_CHOICES,SPECIES_CHOICES



User = get_user_model()


class CharacterTrait(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    

class Allergy(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    


class Disability(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name



class PetProfile(models.Model):
    BREED_CHOICES = DOG_BREEDS + CAT_BREEDS


    name = models.CharField(max_length=100)
    species = models.CharField(max_length=10, choices=SPECIES_CHOICES, default='Dog')
    gender=models.CharField(max_length=50,blank=True, choices=GENDER_CHOICES)
    fosterer = models.ForeignKey('users.CustomUser',on_delete=models.SET_NULL,null=True,blank=True,related_name='fostered_pets')
    size=models.CharField(max_length=50,blank=True, choices=SIZE_CHOICES)
    fur=models.CharField(max_length=50,blank=True, choices=FUR_CHOICES)
    shelter_arrival = models.DateField(null=True, blank=True)
    breed = models.CharField(max_length=50, choices=BREED_CHOICES, blank=True, null=True)    
    age = models.IntegerField()
    character_traits = models.ManyToManyField(CharacterTrait, blank=True)
    allergies = models.ManyToManyField(Allergy, blank=True)
    disabilities = models.ManyToManyField(Disability, blank=True)
    image = models.ImageField(upload_to='pet_photos/', default='pet_photos/default_pet.jpg') 

    def clean(self):
        dog_breeds = [b[0] for b in self.DOG_BREEDS]
        cat_breeds = [b[0] for b in self.CAT_BREEDS]

        if self.species == 'Dog' and self.breed:
            valid_dogs = [b[0] for b in self.DOG_BREEDS]
            if self.breed.lower() not in valid_dogs:
                raise ValidationError("Invalid dog breed for Dog species.")
        elif self.species == 'Cat' and self.breed:
            valid_cats = [b[0] for b in self.CAT_BREEDS]
            if self.breed.lower() not in valid_cats:
                raise ValidationError("Invalid cat breed for Cat species.")
        elif self.species == 'Other' and self.breed:
            raise ValidationError("Breed should be empty for Other species.")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.species}) - {'Available' if not self.fosterer else 'Fostered by ' + self.fosterer.username}"



#can change
class FavoritedPet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ForeignKey(PetProfile, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'pet')  

    def __str__(self):
        return f"{self.user.username} , {self.pet.name}"
    

