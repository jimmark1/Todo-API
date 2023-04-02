from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

#THIS CLASS IS FOR THE CUSTOM USER FIELD THIS RENDERS CUSTOM FIELDS WHAT WE WANT TO SEE ON THE DJANGO ADMIN PANEL

class UserModelAdmin(BaseUserAdmin):
  list_display = ('name','username', 'email', 'is_active', 'is_superuser', 'created_at', 'updated_at')
  list_filter = ('is_superuser',)
  fieldsets = (
      ('User Credentials', {'fields': ('username', 'password')}),
      ('Personal info', {'fields': ('name', 'is_active')}),
      ('Permissions', {'fields': ('is_superuser',)}),
  )
  
  add_fieldsets = (
      (None, {
          'classes': ('wide',),
          'fields': ('email', 'username', 'name', 'is_superuser', 'created_at', 'updated_at'),
      }),
  )
  search_fields = ('name',)
  ordering = ('name','username', 'email', 'is_active', 'is_superuser', 'created_at', 'updated_at')
  filter_horizontal = ()

admin.site.register(UserAccount, UserModelAdmin)