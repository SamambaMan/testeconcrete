# -*- coding: utf-8 -*-
"""Model managers da aplicação"""
from django.db import models
from django.db import transaction
from django.contrib.auth.models import User


class DetalhesUsuarioManager(models.Manager):
    """Model manager para manipulação de usuários e seus detalhes"""

    @staticmethod
    @transaction.atomic
    def adicionarusuario(dados):
        """adiciona um usuário a base já incluindo seus dados"""
        from .models import DetalhesUsuario, Telefone

        novouser = User.objects.create_user(
            dados['email'],
            dados['email'],
            dados['password'])

        novouser.first_name = dados['name']
        novouser.clean()
        novouser.save()

        novodetalhe = DetalhesUsuario()
        novodetalhe.user = novouser

        novodetalhe.clean()
        novodetalhe.save()

        for telefone in dados['phones']:
            novotelefone = Telefone(detalhesusuario=novodetalhe)
            novotelefone.ddd = telefone['ddd']
            novotelefone.numero = telefone['number']
            novotelefone.clean()
            novotelefone.save()

        return novodetalhe

    @staticmethod
    def obterporguid(guid):
        """Obtem um usuário a partir de seu GUID"""
        from .models import DetalhesUsuario

        return DetalhesUsuario.objects.get(guid=guid)
