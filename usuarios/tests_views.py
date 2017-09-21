# -*- coding: utf-8 -*-
"""Módulo de testes das interfaces REST da aplicação"""
from __future__ import unicode_literals
import json
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

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

        response = self.client.post(
            reverse('autenticar'),
            data=self.autenticar_login,
            content_type=JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            reverse('autenticar'),
            data=self.autenticar_login_senha,
            content_type=JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post(
            reverse('autenticar'),
            data=self.autenticar_login_email,
            content_type=JSON_CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
