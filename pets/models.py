from django.core.exceptions import ValidationError
from django.db import models
import random
from django.contrib.auth import get_user_model

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
    SPECIES_CHOICES = [
        ('Dog', 'Dog'),
        ('Cat', 'Cat'),
    ]

    DOG_BREEDS = [
    ('chihuahua', 'Chihuahua'),
    ('labrador', 'Labrador Retriever'),
    ('beagle', 'Beagle'),
    ('husky', 'Siberian Husky'),
    ('poodle', 'Poodle'),
    ('bulldog', 'Bulldog'),
    ('golden_retriever', 'Golden Retriever'),
    ('german_shepherd', 'German Shepherd'),
    ('dachshund', 'Dachshund'),
    ('rottweiler', 'Rottweiler'),
    ('pomeranian', 'Pomeranian'),
    ('shih_tzu', 'Shih Tzu'),
    ('doberman', 'Doberman'),
    ('boxer', 'Boxer'),
    ('great_dane', 'Great Dane'),
    ('border_collie', 'Border Collie'),
    ('corgi', 'Corgi'),
    ('pug', 'Pug'),
    ('other', 'Other')

]
    CAT_BREEDS = [
    ('persian', 'Persian'),
    ('siamese', 'Siamese'),
    ('maine_coon', 'Maine Coon'),
    ('bengal', 'Bengal'),
    ('ragdoll', 'Ragdoll'),
    ('sphynx', 'Sphynx'),
    ('british_shorthair', 'British Shorthair'),
    ('scottish_fold', 'Scottish Fold'),
    ('abyssinian', 'Abyssinian'),
    ('burmese', 'Burmese'),
    ('oriental', 'Oriental'),
    ('american_shorthair', 'American Shorthair'),
    ('russian_blue', 'Russian Blue'),
    ('norwegian_forest', 'Norwegian Forest Cat'),
    ('savannah', 'Savannah'),
    ('tonkinese', 'Tonkinese'),
    ('other', 'Other')

]
    
    SIZE_CHOICES = [
        ('Small','Small'),
        ('Medium','Medium'),
        ('Large','Large')
    ]
    GENDER_CHOICES = [
        ('female', 'Female'),
        ('male', 'Male'),
    ]

    FUR_CHOICES = [
        ('Hairless', 'Hairless'),
        ('Short', 'Short'),
        ('Medium', 'Medium'),
        ('Long', 'Long'),
    ]

    name = models.CharField(max_length=100)
    species = models.CharField(max_length=10, choices=SPECIES_CHOICES, default='Dog')
    gender=models.CharField(max_length=50,blank=True, choices=GENDER_CHOICES)
    fosterer = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fostered_pets'
    )
    size=models.CharField(max_length=50,blank=True, choices=SIZE_CHOICES)
    fur=models.CharField(max_length=50,blank=True, choices=FUR_CHOICES)
    shelter_arrival = models.DateField(null=True, blank=True)


    BREED_CHOICES = DOG_BREEDS + CAT_BREEDS
    breed = models.CharField(
        max_length=50,
        choices=BREED_CHOICES,
        blank=True,
        null=True
    )    
    age = models.IntegerField()
    
    character_traits = models.ManyToManyField(CharacterTrait, blank=True)
    allergies = models.ManyToManyField(Allergy, blank=True)
    disabilities = models.ManyToManyField(Disability, blank=True)
    image = models.ImageField(upload_to='pet_photos/', blank=True, null=True) 

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
        # Optional auto-clear breed for Other species
        if self.species == 'Other':
            self.breed = None
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.name} ({self.species}) - {'Available' if not self.fosterer else 'Fostered by ' + self.fosterer.username}"

class FavoritedPet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ForeignKey(PetProfile, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'pet')  

    def __str__(self):
        return f"{self.user.username} ❤️ {self.pet.name}"
    

