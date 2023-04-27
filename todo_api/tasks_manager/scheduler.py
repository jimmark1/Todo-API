from django.db import connection

def delete_old_data():
    with connection.cursor() as cursor:
        cursor.execute(" DELETE FROM tasks_manager_tasks WHERE created_at < DATE('now', '-1 day') AND  is_completed = true")
