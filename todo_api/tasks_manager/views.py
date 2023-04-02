from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from . models import *

from . serializers import *

class Tasks_manager(APIView):
    
       permission_classes = [permissions.IsAuthenticated]

       def get(self, request):
              try:
                     tasks = Tasks.objects.filter(user=request.user)
                     serializer = Tasks_serializer(tasks, many=True)

                     return Response(serializer.data, status=status.HTTP_200_OK)
              
              except Exception as e:
                     return Response({'error':'Something went wrong while getting tasks'},
                                     status=status.HTTP_400_BAD_REQUEST)

       def post(self, request):
              data = request.data

              if len(data['task_title']) < 3 or data['task_title'].isspace():
                     return Response({'error':'Task title should atleast 3 characters long'},
                            status=status.HTTP_400_BAD_REQUEST)
              
              else:
                     if Tasks.objects.filter(user=request.user, task_title = data['task_title']).exists():
                            return Response({'message':'Tasks already exists'},
                                   status=status.HTTP_400_BAD_REQUEST)
                     else:
                            try:   
                                   Tasks.objects.create(
                                          task_title = data['task_title'].lstrip(),
                                          user = request.user
                                          )
                                
                                   return Response({'success':'Task added sucessfully'}, status=status.HTTP_201_CREATED)

                            except Exception as e:
                                   return Response({'error':'Something went wrong while creating a task'},
                                          status=status.HTTP_400_BAD_REQUEST)
class Task_details(APIView):

       permission_classes = [permissions.IsAuthenticated]

       def put(self, request, pk):
              data = request.data
              instance = Tasks.objects.get(pk=pk)
              serializer = Update_Task_serializer(instance=instance, data=data)

              try:
                     if not data['task_title']:
                            return Response({'error':'Task Title should not be empty'},
                                          status=status.HTTP_400_BAD_REQUEST)
                     else:       
                            if serializer.is_valid():
                                   serializer.save()
                            
                                   return Response({'success':'Task update successfully'},
                                            status=status.HTTP_200_OK)
              except Exception as e:
                     return Response({'error':'Something went wrong while updating tasks'},
                                     status=status.HTTP_400_BAD_REQUEST)


       def delete(self, request, pk):

              if Tasks.objects.filter(pk=pk, user=request.user).exists():
                     try:  
                            task = Tasks.objects.get(pk=pk)
                            task.delete()

                            return Response({'success':'Task deleted successfully'},
                                          status=status.HTTP_200_OK)


                     except Exception as e:
                            return Response({'error':'Something went wrong while deleting tasks'},
                                          status=status.HTTP_400_BAD_REQUEST)
              else:
                     return Response({'error':'Task Does not exists'},
                                          status=status.HTTP_400_BAD_REQUEST)
