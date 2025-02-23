from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import PetProfile

# adding import and export
class PetProfileResource(resources.ModelResource):
    class Meta:
        model = PetProfile
        fields = ('id', 'name', 'species', 'breed', 'age', 'fosterer', 'character_traits', 'allergies', 'disabilities', 'image')


# config for pet profile
@admin.register(PetProfile)
class PetProfileAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = PetProfileResource

    # displayed fields
    list_display = ('name', 'species', 'breed', 'age', 'foster_status', 'fosterer', 'image')

    # for the search bar
    search_fields = ('name', 'species', 'breed', 'fosterer__username')

    # can filter by species age and fosterer
    list_filter = ('species', 'age', ('fosterer', admin.EmptyFieldListFilter)) 

    # display fostering status
    def foster_status(self, obj):
        return "Available" if obj.fosterer is None else f"Fostered"

    foster_status.admin_order_field = 'fosterer'  
    foster_status.short_description = "Foster Status"
