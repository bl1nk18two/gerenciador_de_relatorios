from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
# class Relatorio(models.Model):
#     titulo = models.CharField(max_length=100)
#     conteudo = models.TextField()
#     criado_em = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.titulo


class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, blank=True, null=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Projeto(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    finalizado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} ({self.cliente.nome})"


class Tarefa(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    descricao = models.TextField()
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def duracao(self):
        datetime_inicio = datetime.combine(self.data, self.hora_inicio)
        datetime_fim = datetime.combine(self.data, self.hora_fim)
        return datetime_fim - datetime_inicio

    def __str__(self):
        return f"{self.usuario.username} | {self.data} | {self.projeto.nome} | {self.hora_inicio} - {self.hora_fim}"
    
    
