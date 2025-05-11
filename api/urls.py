from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, GroupViewSet, ClienteViewSet, TarefaViewSet, ProjetoViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'cliente', ClienteViewSet)
router.register(r'tarefa', TarefaViewSet)
router.register(r'projeto', ProjetoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
