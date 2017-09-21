# -*- coding: utf-8 -*-
"""Modulo contendo class exceptions de negócio"""


class ErroAutenticacao(Exception):
    """Erro específico de autenticacao"""
    pass


class ErroAutenticacaoNaoPossivel(Exception):
    """Erro de autenticacao não possível com
    parâmetros informados"""
    pass


class ErroSessaoExpirada(Exception):
    """Erro de sessão de login expirada"""
    pass


class ErroRecursoExistente(Exception):
    """Erro de adicao de recurso já existente"""
    pass


ERRO_MENSAGENS = {
    'erroautenticacao': u'Usuário e/ou senha inválidos',
    'errosessaoexpirada': u"Sessão inválida",
}
