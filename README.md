Teste Concrete Solutions
============
Aplicação para o teste Concrete Solutions:

<a href="https://github.com/concretesolutions/desafio-python/">https://github.com/concretesolutions/desafio-python/</a>

## Instruções:

1.  Instalação do virtualenv (utilizando virtualenvwrapper):
```
        mkvirtualenv testeconcrete
```

A aplicação foi desenvolvida com python 2.7.12, mas foi testada pela ferramenta de Integração Contínua também com 3.5 e roda no ambiente de produção Heroku com 3.5.

2.  Para ativar no virtualenv criado, caso necessário:
```
        workon testeconcrete
```
3.  Instalação dos pacotes do projeto (utilizando pip):
```
        cd testeconcrete
        pip install --upgrade pip
        pip install -r requirements.txt
```
4.  Rodando o check inicial:
```
        ./manage.py check
```
5.  Rodando as migrations iniciais e gerando a base de dados padrão(SQLite):
```
        ./manage.py migrate
```
## Testes:

1.  Para efetuar os testes e extrair o relatório de cobertura:
```
        coverage run manage.py test --pattern=tests*
```
2.  Para gerar o report de cobertura:
```
        coverage report -m
```
3.  Para rodar o pep8:
```
        pep8 .
```
4.  Para testar utilizando o script com curl, execute o servidor em modo de testes:
```
        ./manage.py testserver usuarios
```

Este modo utiliza o banco de dados em memória.

Depois rode o script de testes com o pytest:
```
        pytest pytest -q usuarios/pytest_usuarios.py
```
4.  Endereços:

O repositório online se encontra em:

<a href="https://concreteteste.herokuapp.com/" >https://concreteteste.herokuapp.com/</a>

O endereço da integração contínua rodando os testes unitários da aplicação:

<a href="https://travis-ci.org/SamambaMan/testeconcrete" >https://travis-ci.org/SamambaMan/testeconcrete</a>

## Métodos

        POST - /cadastro/     - Cadastro de Usuários
        POST - /autenticar/   - Método de Login
        GET  - /obter/(guid)/ - Ler dados de Usuário

## Utilização

A aplicação utiliza JWT para autenticação da obtenção de dados de usuário.

Para a execução do método de obtenção, ex:
    
    /obter/(guid, char(40))/

Deve ser passado no HTTP Header:
    
    "Authorization: Bearer (JWT Token)"

A aplicação utiliza como banco de dados local o SQLite, porém, o Heroku não suporta banco de dados no disco efêmero. Então no ambiente de produção estou utilizando Postgresql.
