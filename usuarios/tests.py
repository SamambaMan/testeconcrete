# -*- coding: utf-8 -*-
"""Módulo de testes unitários da aplicação"""
from __future__ import unicode_literals
from django.test import TestCase
from django.db import IntegrityError
from .jwtutils import codificarjwt, decodificarjwt


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

    def test_insercao(self):
        """Testa insercao de um novo usuario"""
        from .models import DetalhesUsuario

        novodetalhe = DetalhesUsuario.objects.adicionarusuario(
            self.usuario_inserir)

        # Testa se gerou o guid
        self.assertIsNotNone(novodetalhe.guid)

        # Testa se gerou o jwt
        self.assertIsNotNone(novodetalhe.jwttoken)

        # Testa se o JWT gerado condiz com o email informado
        token = codificarjwt({'email': novodetalhe.user.username})
        self.assertEquals(token, novodetalhe.jwttoken)

        # Testa se dá erro caso tente inserir um usuário com e-mail idêntico
        with self.assertRaises(IntegrityError):
            novodetalhe = DetalhesUsuario.objects.adicionarusuario(
                self.usuario_inserir)

        # Testa obtenção do usuário inserido no banco
        guid = novodetalhe.guid
        jwttoken = novodetalhe.jwttoken

        obtido = DetalhesUsuario.objects.obterporguid(guid)
        self.assertEqual(obtido.user.username, novodetalhe.user.username)

        # Verifica se o JWT do objeto obtido é idêntico ao antitgo
        self.assertEqual(obtido.jwttoken, jwttoken)

        # Salva o objeto novamente e certifica de que o jwt  e o guid não mudou
        obtido.save()
        self.assertEqual(obtido.jwttoken, jwttoken)
        self.assertEqual(obtido.guid, guid)
