from rest_framework import serializers
from .models import *

from accounts_manager . serializers import UserManagerSerializer

class Tasks_serializer(serializers.ModelSerializer):
       user = UserManagerSerializer()
       
       class Meta:
              model = Tasks
              fields = '__all__'

              extra_kwargs = {'name': {'read_only': False}, 
                              'is_active': {'read_only': False}, 
                              'created_at': {'read_only': False},
                              'updated_at': {'read_only': False},
                              }

class Update_Task_serializer(serializers.ModelSerializer):
       class Meta:
              model = Tasks

              fields = [
                     'task_title',
                     'is_completed'
              ]
              

