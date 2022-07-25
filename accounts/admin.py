from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from accounts.models import UserProfile

from .models import CustomUser

#New by Zander
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class AccountsUserAdmin(AuthUserAdmin):
    def add_view(self, *args, **kwargs):
        self.inlines =[]
        return super(AccountsUserAdmin, self).add_view(*args, **kwargs)

    def change_view(self, *args, **kwargs):
        self.inlines =[UserProfileInline]
        return super(AccountsUserAdmin, self).change_view(*args, **kwargs)


# admin.site.unregister(CustomUser)
admin.site.register(CustomUser, AccountsUserAdmin)


# old by will vincent
# from .forms import CustomUserCreationForm, CustomUserChangeForm
# from django.contrib.auth.admin import UserAdmin

# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = CustomUser
#     list_display = ['email', 'username',]

# admin.site.register(CustomUser, CustomUserAdmin)