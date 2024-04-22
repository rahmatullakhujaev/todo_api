from django.urls import path
from .views import TodoLisApiView,TodoDetailApiView

urlpatterns = [
    path('api/', TodoLisApiView.as_view()),
    path('api/<int:todo_id>/', TodoDetailApiView.as_view())
]