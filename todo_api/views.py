from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsOwner
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework import status
from .models import Todo
from .serializers import TodoSerializers



class TodoLisApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    def get(self, request, *args, **kwargs):
        todos = Todo.objects.filter(user=request.user)
        serializer = TodoSerializers(todos, many=True)
        return Response(serializer.data)


    def post(self, request, *args, **kwargs):
        serializer = TodoSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TodoDetailApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    def get_object(self, user_id, todo_id):
        try:
            todo_instance = Todo.objects.filter(user= user_id).get(id=todo_id)
        except Todo.DoesNotExist:
            todo_instance = None

        return todo_instance
    def get(self, request, todo_id, *args, **kwargs):
        todo_instance = self.get_object(request.user, todo_id)
        if not todo_instance:
            return Response({"error": "todo id does not find"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TodoSerializers(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self, request, todo_id, *args, **kwargs):
        todo_instance = self.get_object(request.user, todo_id)
        if not todo_instance:
            return Response({"error": "todo id does not find"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TodoSerializers(instance=todo_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, todo_id, *args, **kwargs):
        todo_instance = self.get_object(request.user, todo_id)
        if not todo_instance:
            return Response({"error": "todo id does not find"}, status=status.HTTP_400_BAD_REQUEST)
        todo_instance.delete()
        return Response({"message": "Todo succesfully deleted!"})