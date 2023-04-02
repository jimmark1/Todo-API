import uuid
from accounts_manager.models import UserAccount
from django.db import models

class Tasks(models.Model):
       user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True, blank=True)
       task_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
       task_title = models.CharField(max_length=255)

       is_completed = models.BooleanField(default=False)
       created_at = models.DateTimeField(auto_now_add=True)
       updated_at = models.DateTimeField(auto_now_add=True)

       def __str__(self):
              return self.task_title
       
       class Meta:
              ordering = ['is_completed']
    
