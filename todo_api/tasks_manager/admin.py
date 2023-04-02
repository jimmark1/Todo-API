from django.contrib import admin
from .models import *

@admin.register(Tasks)
class AdminTasksManager(admin.ModelAdmin):
       list_display = ('task_title', 'is_completed', 'created_at', 'updated_at')
