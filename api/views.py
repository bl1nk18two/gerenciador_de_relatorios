from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from django.contrib.auth.models import Group, User
from drf_yasg.inspectors import SwaggerAutoSchema
from rest_framework import permissions, viewsets
from drf_yasg.utils import swagger_auto_schema
from django.forms import DateField
from drf_yasg import openapi
import django_filters

from .serializers import GroupSerializer, UserSerializer, ClienteSerializer, ProjetoSerializer, TarefaSerializer
from .models import Cliente, Projeto, Tarefa


# Organização do Swagger
class CustomSwaggerAutoSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        return [getattr(self.view, 'swagger_tag', self.view.__class__.__name__)]


# Filtros
class ClienteFilter(django_filters.FilterSet):
    class Meta:
        model = Cliente
        fields = '__all__'


class TarefaFilter(filters.FilterSet):
    data_inicial = filters.DateFilter(field_name='data', lookup_expr='gte')
    data_final = filters.DateFilter(field_name='data', lookup_expr='lte')

    class Meta:
        model = Tarefa
        fields = ['usuario', 'projeto', 'data', 'data_inicial', 'data_final']

    # Se você quiser customizar o formato da data (DD/MM/YYYY)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'data_inicial' in self.filters:
            self.filters['data_inicial'].field.input_formats = ['%d/%m/%Y']
        if 'data_final' in self.filters:
            self.filters['data_final'].field.input_formats = ['%d/%m/%Y']


# Views
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClienteFilter
    swagger_schema = CustomSwaggerAutoSchema
    swagger_tag = "Clientes"

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('nome', openapi.IN_QUERY, description="Nome do Cliente", type=openapi.TYPE_STRING),
            openapi.Parameter('cpf', openapi.IN_QUERY, description="CPF do Cliente", type=openapi.TYPE_STRING),
            openapi.Parameter('ativo', openapi.IN_QUERY, description="Cliente Ativo?", type=openapi.TYPE_BOOLEAN),
            # Adicione aqui outros campos do filtro, conforme definidos no model
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ProjetoViewSet(viewsets.ModelViewSet):
    queryset = Projeto.objects.all()
    serializer_class = ProjetoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['cliente', 'nome', 'ativo', 'finalizado']
    swagger_schema = CustomSwaggerAutoSchema
    swagger_tag = "Projetos"

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('nome', openapi.IN_QUERY, description="Nome do Projeto", type=openapi.TYPE_STRING),
            openapi.Parameter('cliente', openapi.IN_QUERY, description="ID do Cliente", type=openapi.TYPE_INTEGER),
            openapi.Parameter('ativo', openapi.IN_QUERY, description="Projeto Ativo?", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('finalizado', openapi.IN_QUERY, description="Projeto Finalizado?", type=openapi.TYPE_BOOLEAN),
            # Adicione aqui outros campos do filtro, conforme definidos no model
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class TarefaViewSet(viewsets.ModelViewSet):
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TarefaFilter
    swagger_schema = CustomSwaggerAutoSchema
    swagger_tag = "Tarefas"

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('usuario', openapi.IN_QUERY, description="ID do Usuario", type=openapi.TYPE_INTEGER),
            openapi.Parameter('projeto', openapi.IN_QUERY, description="ID do Projeto", type=openapi.TYPE_INTEGER),
            # openapi.Parameter('data', openapi.IN_QUERY, description="Data (formato: DD/MM/YYYY)", type=openapi.TYPE_STRING),
            openapi.Parameter('data_inicial', openapi.IN_QUERY, description="Data inicial (formato: DD/MM/YYYY)", type=openapi.TYPE_STRING),
            openapi.Parameter('data_final', openapi.IN_QUERY, description="Data final (formato: DD/MM/YYYY)", type=openapi.TYPE_STRING),
            # Adicione aqui outros campos do filtro, conforme definidos no model
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    swagger_schema = CustomSwaggerAutoSchema
    swagger_tag = "Usuários"


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    swagger_schema = CustomSwaggerAutoSchema
    swagger_tag = "Grupos"
