from django.core.exceptions import ValidationError
from django.db import models
import random
from users.models import CustomUser  # Import the custom user model


import random
 
def get_random_image(species):  #Just for testing, assign random images to pets
    """Returns a random image URL based on species."""
    DOG_IMAGES = [
        "https://placedog.net/300/200",
        "https://images.dog.ceo/breeds/husky/n02110185_10047.jpg",
        "https://random.dog/123.jpg"
    ]

    CAT_IMAGES = [
        "https://cataas.com/cat",
        "https://cdn2.thecatapi.com/images/MTY3ODIyMQ.jpg",
        "https://thecatapi.com/api/images/get"
    ]

    OTHER_IMAGES = [
        "https://placebear.com/300/200",
        "https://loremflickr.com/300/200/animal"
    ]

    if species == "Dog":
        return random.choice(DOG_IMAGES)
    elif species == "Cat":
        return random.choice(CAT_IMAGES)
    else:
        return random.choice(OTHER_IMAGES)


class PetProfile(models.Model):
    SPECIES_CHOICES = [
        ('Dog', 'Dog'),
        ('Cat', 'Cat'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    species = models.CharField(max_length=10, choices=SPECIES_CHOICES, default='Dog')
    breed = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField()
    fosterer = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,  # in case there is no fosterer
        related_name='fostered_pets'
    )

    character_traits = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    disabilities = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    def clean(self):
        #checking if the fosterer has been accepted
        if self.fosterer and self.fosterer.fosterer_status != 'accepted':
            raise ValidationError(f"{self.fosterer.username} is not an accepted fosterer and cannot be assigned a pet.")

    def save(self, *args, **kwargs):
        #if the pet doesnt have a photo, assign one of the random ones
        if not self.image:
            self.image = get_random_image(self.species)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.species}) - {'Available' if not self.fosterer else 'Fostered by ' + self.fosterer.username}"
