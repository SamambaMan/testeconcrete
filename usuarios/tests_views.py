# -*- coding: utf-8 -*-
"""Módulo de testes das interfaces REST da aplicação"""
from __future__ import unicode_literals
from datetime import timedelta
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.test.client import RequestFactory
from django.utils.timezone import now
from django.conf import settings
from freezegun import freeze_time
from .views import obter


JSON_CONTENT_TYPE = "application/json"


class CadastrarViewTest(APITestCase):
    """Testes da interface de cadastro de usuario"""

    cadastrar = """{
        "name": "Carlinhos Wesley",
        "email": "carlinhos@grifinoria.com.br",
        "password": "caldadedragão",
        "phones": [
            {
                "number": "987654321",
                "ddd": "21"
            },
            {
                "number": "69686766",
                "ddd": "65"
            }
        ]
    }"""

    def test_cadastro(self):
        """teste de criacao de usuarios"""
        response = self.client.post(
            reverse('cadastro'),
            data=self.cadastrar,
            content_type=JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # testa se o recadastro retorna o erro desejado
        response = self.client.post(
            reverse('cadastro'),
            data=self.cadastrar,
            content_type=JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, 409)


class AutenticarViewTest(APITestCase):
    """Classe de testes de autenticacao"""
    cadastrar_autenticar = """{
        "name": "Rony Wesley",
        "email": "rony@grifinoria.com.br",
        "password": "pastadedentes",
        "phones": [
            {
                "number": "987654321",
                "ddd": "21"
            },
            {
                "number": "69686766",
                "ddd": "65"
            }
        ]
    }"""

    autenticar_login = """{
            "email": "rony@grifinoria.com.br",
            "password": "pastadedentes"
        }

    """

    autenticar_login_senha = """{
            "email": "rony@grifinoria.com.br",
            "password": "sbrubles"
        }

    """

    autenticar_login_email = """{
            "email": "ronyy@grifinoria.com.br",
            "password": "sbrubles"
        }

    """

    def test_autenticacao(self):
        """teste de autenticacao de usuarios"""
        response = self.client.post(
            reverse('cadastro'),
            data=self.cadastrar_autenticar,
            content_type=JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # testa a autenticação direta por usuário e senha
        response = self.client.post(
            reverse('autenticar'),
            data=self.autenticar_login,
            content_type=JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # autenticacao com senha incorreta
        response = self.client.post(
            reverse('autenticar'),
            data=self.autenticar_login_senha,
            content_type=JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # autenticação com email incorreto
        response = self.client.post(
            reverse('autenticar'),
            data=self.autenticar_login_email,
            content_type=JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ObterViewTest(APITestCase):
    """Classe de testes de obtenção de usuarios"""

    cadastrar_obter = """{
        "name": "Gina Wesley",
        "email": "gina@grifinoria.com.br",
        "password": "basilisco",
        "phones": [
            {
                "number": "987654321",
                "ddd": "21"
            },
            {
                "number": "69686766",
                "ddd": "65"
            }
        ]
    }"""

    obter_login = """{
            "email": "gina@grifinoria.com.br",
            "password": "basilisco"
        }

    """

    def setUp(self):
        response = self.client.post(
            reverse('cadastro'),
            data=self.cadastrar_obter,
            content_type=JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        payload = response.data

        self.guid = payload['id']
        self.token = payload['token']

    def test_obtencao(self):
        """teste de obtencao"""

        # Teste utilizando request factory
        request = RequestFactory().get(reverse('obter',
                                               kwargs={"guid": self.guid}))
        request.META['HTTP_AUTHORIZATION'] = "Bearer {0}".format(self.token)
        response = obter(request, self.guid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Testa utilizando o método do próprio método get do Client
        # Repete o teste acima de forma melhorada
        response = self.client.get(
            reverse('obter', kwargs={"guid": self.guid}),
            HTTP_AUTHORIZATION="Bearer {0}".format(self.token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_invalido(self):
        """teste de token invalido"""

        request = RequestFactory().get(reverse('obter',
                                               kwargs={"guid": self.guid}))
        request.META['HTTP_AUTHORIZATION'] = "Bearer {0}".format("sonserina")
        response = obter(request, self.guid)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Testa utilizando o método do próprio método get do Client
        # Repete o teste acima de forma melhorada
        response = self.client.get(
            reverse('obter', kwargs={"guid": self.guid}),
            HTTP_AUTHORIZATION="Bearer {0}".format("corvinal"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_guid_invalido(self):
        """ testa guid invalido """
        request = RequestFactory().get(reverse('obter',
                                               kwargs={"guid": "corvinal"}))
        request.META['HTTP_AUTHORIZATION'] = "Bearer {0}".format(self.token)
        response = obter(request, "corvinal")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Testa utilizando o método do próprio método get do Client
        # Repete o teste acima de forma melhorada
        response = self.client.get(
            reverse('obter', kwargs={"guid": "lufalufa"}),
            HTTP_AUTHORIZATION="Bearer {0}".format(self.token))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_sessao_invalida(self):
        """ testa obtencao de um token com hora adiantada e sessao expirada """

        with freeze_time(now() + timedelta(seconds=settings.TEMPO_SESSAO + 1)):
            request = RequestFactory().get(reverse('obter',
                                                   kwargs={"guid": self.guid}))
            request.META['HTTP_AUTHORIZATION'] = "Bearer {0}".format(
                self.token)
            response = obter(request, self.guid)
            self.assertEqual(response.status_code, 440)

            # Testa utilizando o método do próprio método get do Client
            # Repete o teste acima de forma melhorada
            response = self.client.get(
                reverse('obter', kwargs={"guid": self.guid}),
                HTTP_AUTHORIZATION="Bearer {0}".format(self.token))
            self.assertEqual(response.status_code, 440)
