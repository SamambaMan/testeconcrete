# -*- coding: utf-8 -*-
"""Funções para codificação/decodificação de JWT"""
import jwt
from django.conf import settings

ALGORITHM = "HS256"

def codificarjwt(payload):
    """Codifica de acordo com um Payload o JWT"""
    return jwt.encode(payload, settings.SECRET_KEY, ALGORITHM)

def decodificarjwt(chavejwt):
    """Decodifica uma chave JWT"""
    return jwt.decode(chavejwt, settings.SECRET_KEY, ALGORITHM)
