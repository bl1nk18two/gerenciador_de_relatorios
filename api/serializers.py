import re

from django.contrib.auth.models import Group, User
from rest_framework import serializers

from .models import Cliente, Projeto, Tarefa


class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )    

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups'] 


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

    def validate_cnpj(self, value):
        cnpj_tratado = re.sub(r'/D', '', value)
        tamanho_cnpj_tratado = len(cnpj_tratado)
        if tamanho_cnpj_tratado != 14:
            raise serializers.ValidationError(f'O CNPJ deve conter 14 digitos, não {tamanho_cnpj_tratado}.')
        return cnpj_tratado

    def validate_nome(self, value):
        return value.upper()


class ProjetoSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Projeto
        fields = '__all__'


class TarefaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarefa
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Torna o campo 'projeto' opcional
        self.fields['projeto'].required = False
        
    def validate_projeto(self, value):
        if not value:
            return None
        return value

    def validate(self, data):
        # Método geral de validação - será sempre chamado
        # Se 'projeto' não for fornecido na requisição, adiciona como None
        if 'projeto' not in data:
            data['projeto'] = None
        return data    