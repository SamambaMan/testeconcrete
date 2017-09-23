"""Modulo de testes integrados da aplicacao"""
import requests

SERVIDOR = 'http://localhost:8000/{0}'


class TestCadastro(object):
    """Testes relacionados a cadastro de usuarios"""

    payload = """{
        "name": "Felipe Ferreira",
        "password": "umasenha",
        "email": "felipe.gomes@test.com",
        "phones": [
            {
                "ddd": "21",
                "number": "92928374"
            }
        ]
    }"""

    def test_cadastrar(self):
        """testa o cadastro dos usuarios"""
        retorno = requests.post(SERVIDOR.format("cadastro/"),
                                data=self.payload)
        assert retorno.status_code == 201

        # testa o recadastro
        retorno = requests.post(SERVIDOR.format("cadastro/"),
                                data=self.payload)
        assert retorno.status_code == 409


class TestAutenticacao(object):
    """Teste de autenticacao de usuario"""
    payload = """{
        "name": "Draco Malfoy",
        "password": "outrasenha",
        "email": "draco.malfoy@test.com",
        "phones": [
            {
                "ddd": "21",
                "number": "92928374"
            }
        ]
    }"""

    login = """{
        "email": "draco.malfoy@test.com",
        "password": "outrasenha"
    }"""

    login_invalido = """{
        "email": "draco.malfoy@test.com",
        "password": "senhainvalida"
    }"""

    def setup(self):
        """inicializa o teste"""
        requests.post(SERVIDOR.format("cadastro/"),
                      data=self.payload)

    def test_autenticacao(self):
        """teste de autenticacao com sucesso"""
        retorno = requests.post(SERVIDOR.format("autenticar/"),
                                data=self.login)
        assert retorno.status_code == 200

    def test_senha_invalida(self):
        """teste de autenticacao com falha"""
        retorno = requests.post(SERVIDOR.format("autenticar/"),
                                data=self.login_invalido)
        assert retorno.status_code == 401


class TestObtencao(object):
    """Testa a obtencao de usuarios"""

    payload = """{
        "name": "Ronald Weasley",
        "password": "outrasenha",
        "email": "ronald.weasley@test.com",
        "phones": [
            {
                "ddd": "21",
                "number": "92928374"
            }
        ]
    }"""

    login = """{
        "email": "ronald.weasley@test.com",
        "password": "outrasenha"
    }"""

    email = "ronald.weasley@test.com"

    token_invalido = {"Authorization": "Bearer gina"}

    guid = None
    token = None
    metodo = None
    header = None

    def setup_class(self):
        """inicializa o teste"""
        response = requests.post(SERVIDOR.format("cadastro/"),
                                 data=self.payload)

        data = response.json()

        if "id" not in data.keys():
            return

        self.guid = data["id"]
        self.token = data["token"]
        self.metodo = "obter/{0}/".format(self.guid)
        self.header = {"Authorization": "Bearer {0}".format(self.token)}

    def test_obter_sucesso(self):
        """pega um usuario"""
        print SERVIDOR.format(self.metodo)
        response = requests.get(SERVIDOR.format(self.metodo),
                                data=self.payload,
                                headers=self.header)

        assert response.status_code == 200

        dados = response.json()

        assert dados['email'] == self.email

    def test_obter_falha_token(self):
        """ verifica erro de token invalido"""
        response = requests.get(SERVIDOR.format(self.metodo),
                                data=self.payload,
                                headers=self.token_invalido)

        assert response.status_code == 401

    def test_obter_falha_guid(self):
        """ verifica erro de guid invalido"""
        response = requests.get(SERVIDOR.format("obter/guidinvalido/"),
                                data=self.payload,
                                headers=self.header)

        assert response.status_code == 401
