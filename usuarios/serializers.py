"""Serializers utilizados nas views"""

try:
    unicode
except:
    unicode = str


def serializaerro(mensagem):
    """Serializa qualquer mensagem de erro"""
    return {'mensagem': unicode(mensagem)}


FDATA = '%Y-%m-%d %H:%M:%S'


def serializarusuario(usuario):
    jwttoken = usuario.gerajwt()

    try:
        jwttoken = a.decode('UTF-8')
    except:
        pass
    retorno = {
        'name': unicode(usuario.user.first_name),
        'email': unicode(usuario.user.username),
        'id': usuario.guid,
        'created': usuario.user.date_joined.strftime(FDATA),
        'modified': usuario.ultimamodificacao.strftime(FDATA),
        'last_login': usuario.user.last_login.strftime(FDATA),
        'token': jwttoken
        }
    phones = []
    for telefone in usuario.telefone_set.all():
        phones += [{'number': unicode(telefone.numero),
                    'ddd': unicode(telefone.ddd)}]
    retorno['phones'] = phones

    return retorno
