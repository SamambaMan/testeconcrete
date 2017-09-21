# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .exceptions import ErroAutenticacao, ErroAutenticacaoNaoPossivel,\
                        ErroSessaoExpirada, ErroRecursoExistente
from .models import DetalhesUsuario
from .serializers import serializaerro, serializarusuario


def parsepayload(payload):
    """Transforma os bodys em payloads da aplicação"""
    body_unicode = payload.decode('utf-8')
    return json.loads(body_unicode)


def trataerros(metodo):
    """Tratamento de exceptions e retorno de códigos HTTP"""
    def func_wrapper(*args, **kwargs):
        """Decorator wrapper"""
        try:
            return metodo(*args, **kwargs)
        except ErroAutenticacao as erro:
            return Response(serializaerro(erro),
                            status=status.HTTP_401_UNAUTHORIZED)
        except ErroAutenticacaoNaoPossivel as erro:
            return Response(serializaerro(erro),
                            status=status.HTTP_401_UNAUTHORIZED)
        except ErroSessaoExpirada as erro:
            return Response(serializaerro(erro),
                            status=440)
        except ErroRecursoExistente as erro:
            return Response(serializaerro(erro),
                            status=409)
        except Exception as error:
            return Response(serializaerro(
                u"Ocorreu um erro não tratado: " + str(error)),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return func_wrapper


@api_view(['POST'])
@trataerros
def cadastro(request):
    """Interface rest de cadastro de usuarios"""
    payload = parsepayload(request.body)

    usuario = DetalhesUsuario.objects.adicionarusuario(payload)

    return Response(serializarusuario(usuario), status.HTTP_201_CREATED)


@api_view(['POST'])
@trataerros
def autenticar(request):
    """Autentica um usuário"""
    payload = parsepayload(request.body)

    usuario = DetalhesUsuario.objects.autenticar(payload['email'],
                                                 payload['password'])

    return Response(serializarusuario(usuario), status.HTTP_200_OK)


@api_view(['GET'])
@trataerros
def obter(request, guid):
    """Obtem um usuário a partir de seu guid/token"""
    jwttoken = request.META['HTTP_AUTHORIZATION']

    jwttoken = jwttoken.split(' ')[1]

    # compatibilizacao python 2/3
    if isinstance(jwttoken, bytes):
        jwttoken = jwttoken.decode('UTF-8')

    usuario = DetalhesUsuario.objects.obterporguidetoken(guid, jwttoken)

    return Response(serializarusuario(usuario), status.HTTP_200_OK)
