# -*- coding: utf-8 -*-
"""Model managers da aplicação"""
from django.db import models, transaction, IntegrityError
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from .exceptions import ErroRecursoExistente, ErroAutenticacao, ErroSessaoExpirada,\
                        ErroAutenticacaoNaoPossivel, ERRO_MENSAGENS
from .jwtutils import hashjwt


class DetalhesUsuarioManager(models.Manager):
    """Model manager para manipulação de usuários e seus detalhes"""

    @staticmethod
    @transaction.atomic
    def adicionarusuario(dados):
        """adiciona um usuário a base já incluindo seus dados"""
        from .models import DetalhesUsuario, Telefone

        if DetalhesUsuario.objects.filter(
                user__username=dados['email']).exists():
            raise ErroRecursoExistente(u"E-mail já existente")

        novouser = User.objects.create_user(
            dados['email'],
            dados['email'],
            dados['password'])

        novouser.first_name = dados['name']
        novouser.last_login = now()
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

    @staticmethod
    def obterporguidetoken(guid, token):
        """obtem um usuário a partir de seu guid e token  de sessão válido"""
        from .models import DetalhesUsuario

        usuario = None
        try:
            usuario = DetalhesUsuario.objects.get(jwttoken=hashjwt(token))
        except:
            raise ErroAutenticacao(ERRO_MENSAGENS['erroautenticacao'])

        if usuario.guid != guid:
            raise ErroAutenticacao(ERRO_MENSAGENS['erroautenticacao'])

        diferenca = now() - usuario.user.last_login
        if diferenca.total_seconds() > settings.TEMPO_SESSAO:
            raise ErroSessaoExpirada(ERRO_MENSAGENS['errosessaoexpirada'])

        return usuario

    @staticmethod
    @transaction.atomic
    def autenticar(email, senha):
        """autentica o usuário de acordo com os dados informados e
        atualiza seus dados"""
        from .models import DetalhesUsuario

        try:
            usuario = DetalhesUsuario.objects.get(user__username=email)
        except ObjectDoesNotExist:
            raise ErroAutenticacao(ERRO_MENSAGENS['erroautenticacao'])

        if not usuario.user.check_password(senha):
            raise ErroAutenticacaoNaoPossivel(
                ERRO_MENSAGENS['erroautenticacao'])

        usuario.user.last_login = now()
        usuario.user.save()

        usuario.save()

        return usuario
