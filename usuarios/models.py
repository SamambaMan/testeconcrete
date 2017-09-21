# -*- coding: utf-8 -*-
"""Módulo com os modelos da aplicação"""
from __future__ import unicode_literals
import hashlib
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from .jwtutils import codificarjwt, hashjwt
from .managers import DetalhesUsuarioManager


class DetalhesUsuario(models.Model):
    """Modelo para especialização do django auth.user"""
    user = models.OneToOneField(User)
    guid = models.CharField(max_length=40)
    jwttoken = models.CharField(max_length=40)
    ultimamodificacao = models.DateTimeField(default=now)
    objects = DetalhesUsuarioManager()

    def save(self, *args, **kwargs):
        """Sobrecarga do método save, para incrementar valores de token e
        guid"""
        if not self.guid:
            self.guid = hashlib.sha1(
                self.user.username.encode('utf-8')).hexdigest()

        if not self.jwttoken:
            jwtcodificado = self.gerajwt()
            self.jwttoken = hashjwt(jwtcodificado)

        self.ultimamodificacao = now()

        super(DetalhesUsuario, self).save(*args, **kwargs)

    def verificajwt(self, jwttoken):
        """Verifica se um token jwt informado é igual a
        hash inserida no banco"""
        return hashlib.sha1(jwttoken).hexdigest() == self.jwttoken

    def gerajwt(self):
        """Gera o JWT deste usuário a partir de seu e-mail"""
        return codificarjwt({'email': self.user.username})


class Telefone(models.Model):
    """Armazena o telefone de um usuario"""
    detalhesusuario = models.ForeignKey(DetalhesUsuario)
    ddd = models.CharField(max_length=2)
    numero = models.CharField(max_length=9)
