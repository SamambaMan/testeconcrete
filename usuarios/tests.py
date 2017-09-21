# -*- coding: utf-8 -*-
"""Módulo de testes unitários da aplicação"""
from __future__ import unicode_literals
from datetime import timedelta
from django.test import TestCase
from django.db import IntegrityError
from django.utils.timezone import now
from django.conf import settings
from freezegun import freeze_time
from .jwtutils import codificarjwt, decodificarjwt
from .models import DetalhesUsuario
from .exceptions import ErroSessaoExpirada, ErroAutenticacao,\
                        ErroAutenticacaoNaoPossivel, ErroRecursoExistente


class TesteJWT(TestCase):
    """Testes de JWT"""

    def test_codificacao(self):
        """Testa a codificação e decodificação JWT"""
        payload = {'algum': 'payload'}
        outropayload = {'outro': 'payload'}
        codificado = codificarjwt(payload)
        decodificado = decodificarjwt(codificado)
        self.assertEquals(payload, decodificado)
        self.assertNotEquals(outropayload, decodificado)


class TesteUsuario(TestCase):
    """Testes relacionados a CRUD de usuários"""

    usuario_inserir = {
        "name": "João da Silva",
        "email": "joao@silva.org",
        "password": "hunter2",
        "phones": [
            {
                "number": "987654321",
                "ddd": "21"
            }
        ]
    }

    usuario_autenticacao = {
        "name": "Fulano Ciclano",
        "email": "fulano@ciclano.org",
        "password": "senhatensa",
        "phones": [
        ]
    }

    usuario_guidtoken = {
        "name": "Beltrano Ciclano",
        "email": "beltrano@ciclano.org",
        "password": "outrasenha",
        "phones": [
        ]
    }

    def test_insercao(self):
        """Testa insercao de um novo usuario"""

        novodetalhe = DetalhesUsuario.objects.adicionarusuario(
            self.usuario_inserir)

        # Testa se gerou o guid
        self.assertIsNotNone(novodetalhe.guid)

        # Testa se gerou o jwt
        self.assertIsNotNone(novodetalhe.jwttoken)

        # Testa se o JWT gerado condiz com o email informado
        token = codificarjwt({'email': novodetalhe.user.username})
        self.assertTrue(novodetalhe.verificajwt(token))

        # Testa se dá erro caso tente inserir um usuário com e-mail idêntico
        with self.assertRaises(ErroRecursoExistente):
            novodetalhe = DetalhesUsuario.objects.adicionarusuario(
                self.usuario_inserir)

        # testa a reinsercao de um usuario
        with self.assertRaises(ErroRecursoExistente):
            DetalhesUsuario.objects.adicionarusuario(
                self.usuario_inserir)

        # Testa obtenção do usuário inserido no banco
        guid = novodetalhe.guid
        jwttoken = novodetalhe.jwttoken

        obtido = DetalhesUsuario.objects.obterporguid(guid)
        self.assertEqual(obtido.user.username, novodetalhe.user.username)

        # Verifica se o JWT do objeto obtido é idêntico ao antitgo
        self.assertEqual(obtido.jwttoken, jwttoken)

        dataanterior = obtido.ultimamodificacao
        obtido.save()

        # Salva o objeto novamente e certifica de que o jwt  e o guid não mudou
        self.assertTrue(obtido.verificajwt(token))
        self.assertEqual(obtido.guid, guid)

        # Verifica se a data mudou
        self.assertTrue(dataanterior < obtido.ultimamodificacao)

    def test_autenticacao(self):
        """Testes de autenticação de usuário e senha"""
        DetalhesUsuario.objects.adicionarusuario(
            self.usuario_autenticacao)

        # Testa email inexistente
        with self.assertRaises(ErroAutenticacao):
            DetalhesUsuario.objects.autenticar(
                "sbrubles",
                self.usuario_autenticacao['password']
            )

        # Testa email existente com senha invalida
        with self.assertRaises(ErroAutenticacaoNaoPossivel):
            DetalhesUsuario.objects.autenticar(
                self.usuario_autenticacao['email'],
                "sbrubles"
            )

        # Autentica tudo bonito
        autenticado = DetalhesUsuario.objects.autenticar(
            self.usuario_autenticacao['email'],
            self.usuario_autenticacao['password']
        )

        # Verifica se o email do usuario retornado é igual ao informado
        self.assertEqual(autenticado.user.username,
                         self.usuario_autenticacao['email'])

    def test_guid_token(self):
        """testa a obtencao de usuario por guid e token"""
        novo = DetalhesUsuario.objects.adicionarusuario(
            self.usuario_guidtoken)

        token = codificarjwt({'email': self.usuario_guidtoken['email']})

        # Asserta se o token gerado é igual ao token informado pelo modelo
        self.assertEqual(token, novo.gerajwt())

        # Verifica erro de sessão expirada
        with freeze_time(now() + timedelta(seconds=settings.TEMPO_SESSAO + 1)):
            with self.assertRaises(ErroSessaoExpirada):
                DetalhesUsuario.objects.obterporguidetoken(novo.guid, token)

        # Busca por token inexistente
        tokeninexistente = codificarjwt({'email': 'lorenipson@lero.com'})
        with self.assertRaises(ErroAutenticacao):
            DetalhesUsuario.objects.obterporguidetoken(novo.guid,
                                                       tokeninexistente)

        # token certo e válido, mas guid inexistente
        with self.assertRaises(ErroAutenticacao):
            DetalhesUsuario.objects.obterporguidetoken('GUIDGUIDGUIDGUID',
                                                       token)

        # certifica de que o usuário é o que deveria vir
        usuario = DetalhesUsuario.objects.obterporguidetoken(novo.guid, token)
        self.assertEqual(usuario.user.username,
                         self.usuario_guidtoken['email'])
