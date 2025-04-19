from django.db.models import Count
from django.db import models


def suggest_pets_for_user(user):
    from pets.models import PetProfile

    if not hasattr(user, 'ideal_pet_profile'):
        if not hasattr(user, 'ideal_pet_profile'):
            print("No ideal pet profile found.")
        return PetProfile.objects.none()

    ideal = user.ideal_pet_profile
    pets = PetProfile.objects.filter(fosterer__isnull=True)

    if ideal.species and ideal.species.strip().lower() == 'dog':
        if ideal.dog_breed and ideal.dog_breed.strip():
                pets = pets.filter(breed__iexact=ideal.dog_breed.strip())
    elif ideal.species and ideal.species.strip().lower() == 'cat':
        if ideal.cat_breed and ideal.cat_breed.strip():
            pets = pets.filter(breed__iexact=ideal.cat_breed.strip())


    if ideal.min_age is not None:
        pets = pets.filter(age__gte=ideal.min_age)

    if ideal.max_age is not None and ideal.max_age != 0:
        pets = pets.filter(age__lte=ideal.max_age)

    if ideal.gender and ideal.gender.strip():
        pets = pets.filter(gender__iexact=ideal.gender.strip())

    if ideal.size and ideal.size.strip():
        pets = pets.filter(size__iexact=ideal.size.strip())

    if ideal.character_traits.exists():
        selected_traits = ideal.character_traits.all()
        pets = pets.annotate(
            match_count=Count('character_traits', filter=models.Q(character_traits__in=selected_traits), distinct=True)
        ).filter(match_count=selected_traits.count())

    if ideal.disabilities.exists():
        pets = pets.filter(disabilities__in=ideal.disabilities.all())


    return pets

