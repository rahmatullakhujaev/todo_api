from django.urls import path, include
from .views import TodoLisApiView,TodoDetailApiView, TodoViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('api-viewset', TodoViewSet,)

urlpatterns = [
    path('api/', TodoLisApiView.as_view()),
    path('api/<int:todo_id>/', TodoDetailApiView.as_view()),
    path('', include(router.urls))
]