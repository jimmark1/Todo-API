from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

class UserManagerSerializer(serializers.ModelSerializer):
       name = serializers.ReadOnlyField()
       class Meta:
              model = User

              fields = [
                     'name',
                     'is_active',
                     'created_at',
                     'updated_at'
              ]