# -*- coding: utf-8 -*-
"""Módulo com os modelos da aplicação"""
from __future__ import unicode_literals
import hashlib
import random
from django.db import models
from django.contrib.auth.models import User
from .jwtutils import codificarjwt
from .managers import DetalhesUsuarioManager


class DetalhesUsuario(models.Model):
    """Modelo para especialização do django auth.user"""
    user = models.OneToOneField(User)
    guid = models.CharField(max_length=40)
    jwttoken = models.TextField()
    objects = DetalhesUsuarioManager()

    def save(self, *args, **kwargs):
        """Sobrecarga do método save, para incrementar valores de token e
        guid"""
        if not self.guid:
            self.guid = hashlib.sha1(str(random.random())).hexdigest()

        if not self.jwttoken:
            self.jwttoken = codificarjwt({'email': self.user.username})

        super(DetalhesUsuario, self).save(*args, **kwargs)


class Telefone(models.Model):
    """Armazena o telefone de um usuario"""
    detalhesusuario = models.ForeignKey(DetalhesUsuario)
    ddd = models.CharField(max_length=2)
    numero = models.CharField(max_length=9)
