from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'cliente', views.ClienteViewSet)
router.register(r'tarefa', views.TarefaViewSet)
router.register(r'projeto', views.ProjetoViewSet)

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('', include(router.urls)),
]
