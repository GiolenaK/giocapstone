from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import CustomUser

# Import export function
class UserResource(resources.ModelResource):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'user_type', 'fosterer_status', 'profile_photo', 'date_joined')

# register user
@admin.register(CustomUser)
class CustomUserAdmin(ImportExportModelAdmin, UserAdmin):
    resource_class = UserResource

    # fields displayed
    list_display = ('username', 'email', 'user_type', 'fosterer_status', 'profile_photo', 'is_active', 'date_joined')

    # for search bar
    search_fields = ('username', 'email', 'user_type', 'fosterer_status')

    # filter by user type, foster status and activity
    list_filter = ('user_type', 'fosterer_status', 'is_active')

    # defining the new user fields when creating new users
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('user_type', 'fosterer_status', 'profile_photo')}),
    )

    # adding these fields
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('user_type', 'fosterer_status', 'profile_photo')}),
    )
