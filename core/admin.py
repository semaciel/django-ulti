from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import User, CityModel, AddressModel

# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# class UserAdmin(BaseUserAdmin):
class UserAdmin(admin.ModelAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display=('username','first_name','last_name','is_active','date_joined', 'email', 'is_email_verified', 'is_staff', 'is_superuser', 'role')
    search_fields =('username','first_name','last_name','is_active','date_joined', 'email', 'is_email_verified', 'is_staff', 'is_superuser', 'role')
    list_per_page=25

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser:
            form.base_fields['username'].disabled = True
            form.base_fields['is_superuser'].disabled = True
            form.base_fields['user_permissions'].disabled = True
            form.base_fields['groups'].disabled = True
        return form

admin.site.register(User, UserAdmin)
admin.site.register(CityModel)
admin.site.register(AddressModel)
# admin.site.register(TrackingModel)
