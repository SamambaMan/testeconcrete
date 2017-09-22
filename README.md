Teste Concrete Solutions
============
Aplicação para o teste Concrete Solutions

## Instruções:

1.  Instalação do virtualenv (utilizando virtualenvwrapper):
```
        mkvirtualenv testeconcrete
```
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
5.  Rodando as migrations iniciais e gerando a base de dados padrão:
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

## Métodos

        POST - /cadastro/     - Cadastro de Usuários
        POST - /autenticar/   - Método de Login
        GET  - /obter/(guid)/ - Ler dados de Usuário
