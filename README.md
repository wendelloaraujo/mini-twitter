
# Mini-Twitter API

Este projeto implementa uma API RESTful para uma plataforma de mídia social simples, semelhante ao Twitter. A API permite que os usuários registrem-se, autentiquem-se, publiquem, curtam postagens, sigam outros usuários e vejam um feed com postagens de usuários que seguem.

## 🏁 Funcionalidades Implementadas

- Registro de usuário e autenticação via JWT.
- Criação, edição, exclusão e curtida de postagens.
- Seguir e deixar de seguir outros usuários.
- Exibição de feed de postagens de usuários seguidos com paginação.
- Cache para melhorar a escalabilidade das requisições do feed.
- Contagem de curtidas e seguidores em tempo real.
- Testes automatizados com cobertura completa de código.
- Uso de Docker para configuração e execução do projeto.
- Documentação da API gerada com Swagger.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.12.7
- **Framework:** Django REST Framework
- **Banco de Dados:** PostgreSQL
- **Cache:** Redis
- **Filas Assíncronas:** Celery
- **Autenticação:** JWT
- **Documentação da API:** Swagger
- **CI/CD:** GitHub Actions

## 📦 Pré-requisitos

Antes de iniciar, certifique-se de ter as seguintes ferramentas instaladas:

- Docker
- Docker Compose
- Python 3.12.7

## 🚀 Configuração do Projeto

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/mini-twitter.git
cd mini-twitter
```

2. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
SECRET_KEY='sua-chave-secreta-aqui'
DB_NAME='postgres'
DB_USER='postgres'
DB_PASSWORD='postgres'
DB_HOST='db'
DB_PORT=5432
REDIS_HOST='redis'
EMAIL_HOST='localhost'
DEFAULT_FROM_EMAIL='webmaster@localhost'
```

3. Inicie o Docker:

```bash
docker-compose up --build
```

4. Acesse o projeto em [http://localhost:8000](http://localhost:8000).

## 🧪 Executando Testes

Para executar os testes automatizados e verificar a cobertura de código, use:

```bash
docker-compose run test
```

Os resultados da cobertura serão gerados na pasta `htmlcov`.

## 📜 Gerando a Documentação da API

A documentação da API é gerada automaticamente usando o Swagger. Para acessá-la, siga para [http://localhost:8000/swagger/](http://localhost:8000/swagger/) após iniciar o projeto.

## 📚 Diagrama de Arquitetura e ERD

1. **Diagrama de Arquitetura:** Explica como os componentes do sistema se integram, incluindo Django, PostgreSQL, Redis, e Celery para tarefas assíncronas.
2. **Diagrama ERD:** Representa o relacionamento entre as entidades principais, como `User`, `Post`, `Like`, `Follow`, e `Profile`.

## 🐳 Comandos Úteis do Docker

- Para reiniciar o projeto: `docker-compose restart`
- Para parar os serviços: `docker-compose down`
- Para acessar o contêiner do Django: `docker-compose exec web bash`

## 📧 Suporte

Para qualquer dúvida ou problema, entre em contato em [seu-email@dominio.com](mailto:seu-email@dominio.com).

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 📝 Licença

Este projeto está sob a licença MIT.
