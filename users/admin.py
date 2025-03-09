from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.shortcuts import redirect


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



    def response_change(self, request, obj):
    
        if obj.user_type in ["admin", "staff"] and obj.fosterer_status != "none":  #raise an error if the user type is admin or staff and fosterer status is not none
            self.message_user(
                request,
                "Admin and Staff users cannot have a Fosterer Status, it will be reset to 'None'.",messages.ERROR,)
            
            obj.fosterer_status = "none"  
            obj.save()  
            return redirect(request.path)  
        
        return super().response_change(request, obj)