# 🐦 Mini-Twitter API

Este projeto implementa uma API RESTful para uma plataforma de mídia social simples, semelhante ao Twitter. A API permite que os usuários registrem-se, autentiquem-se, publiquem, curtam postagens, sigam outros usuários e vejam um feed com postagens de usuários que seguem.

## 📑 Índice

- [🛠️ Tecnologias Utilizadas](#️-tecnologias-utilizadas)
- [✨ Funcionalidades](#-funcionalidades)
- [📋 Pré-requisitos](#-pré-requisitos)
- [🚀 Configuração e Execução](#-configuração-e-execução)
- [✅ Testes](#-testes)
- [📄 Documentação da API](#-documentação-da-api)
- [📊 Diagramas](#-diagramas)
- [🐳 Comandos Úteis do Docker](#-comandos-úteis-do-Docker)
- [📧 Suporte](#-suporte)
- [👤 Autor](#-autor)

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.12.7
- **Framework:** Django REST Framework
- **Banco de Dados:** PostgreSQL
- **Autenticação:** JWT (JSON Web Tokens)
- **Cache:** Redis
- **Filas Assíncronas:** Celery
- **Conteinerização:** Docker e Docker Compose
- **Documentação da API:** Swagger
- **Testes:** Pytest
- **CI/CD:** GitHub Actions

## ✨ Funcionalidades

- Registro e autenticação de usuários usando JWT
- Seguir e deixar de seguir outros usuários
- Criação, edição e exclusão de posts com texto e imagem
- Curtir e descurtir posts
- Visualização de um feed personalizado com posts dos usuários seguidos
- Paginação dos posts no feed
- Busca de posts por palavra-chave ou nome de usuário
- Cache do feed do usuário usando Redis
- Restrição de requisições para evitar excesso de acesso (limitação de taxa)
- Envio de notificações por email ao seguir um usuário
- Cobertura completa de código de testes com Pytest
- Pipeline de CI/CD com GitHub Actions
- Documentação da API gerada com Swagger

## 📋 Pré-requisitos

Antes de iniciar, certifique-se de ter as seguintes ferramentas instaladas:

- Docker
- Docker Compose
- Python 3.12.7

## 🚀 Configuração e Execução

### 1. Clonar o Repositório

```bash
git clone https://github.com/seu_usuario/mini-twitter.git
cd mini-twitter
```

### 2. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
SECRET_KEY=sua_chave_secreta
DB_NAME=nome_do_banco
DB_USER=usuario_do_banco
DB_PASSWORD=senha_do_banco
DB_HOST=db
DB_PORT=5432
REDIS_HOST=redis
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=seu_email@example.com
EMAIL_HOST_PASSWORD=sua_senha_de_email
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=seu_email@example.com
```

**Notas:**

- **SECRET_KEY:** Uma chave secreta para sua instância do Django. Você pode gerar uma usando ferramentas online ou comandos do Django.
- **EMAIL\_\***: Você pode usar um serviço de email como o **Mailtrap** para testes de envio de email em ambiente de desenvolvimento.

### 3. Construir e Iniciar os Containers

No terminal, execute:

```bash
docker-compose up --build
```

Este comando irá:

- Construir as imagens Docker necessárias.
- Iniciar os serviços definidos no `docker-compose.yml` (web, db, redis, celery).

### 4. Aplicar Migrações e Criar Superusuário (Opcional)

Em um novo terminal, execute:

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

- **Migrar o Banco de Dados:** Aplica as migrações para criar as tabelas necessárias no banco de dados.
- **Criar Superusuário:** Cria um usuário administrador para acessar o painel de administração do Django.

### 5. Acessar a Aplicação

- **API:** [http://localhost:8000/api/](http://localhost:8000/api/)
- **Documentação Swagger:** [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- **Admin Django:** [http://localhost:8000/admin/](http://localhost:8000/admin/) (se o superusuário foi criado)

## ✅ Testes

Para executar os testes com cobertura de código, use o serviço `test` definido no `docker-compose.yml`:

```bash
docker-compose run test
```

Este comando irá:

- Executar os testes definidos na pasta `api/tests/` usando o **pytest**.
- Gerar um relatório de cobertura em HTML no diretório `htmlcov/`.

### Visualizar o Relatório de Cobertura

Você pode abrir o arquivo `htmlcov/index.html` em um navegador para visualizar o relatório detalhado.

```bash
xdg-open htmlcov/index.html
```

**Nota:** O comando acima funciona no Linux. No Windows ou macOS, abra o arquivo manualmente ou use o comando apropriado.

## 📄 Documentação da API

A documentação da API está disponível via Swagger no endpoint:

[http://localhost:8000/swagger/](http://localhost:8000/swagger/)

Nesta documentação, você pode visualizar todos os endpoints disponíveis, seus métodos, parâmetros e modelos de dados. Através da interface Swagger, você também pode testar as requisições diretamente no navegador.

## 📊 Diagramas

### 📌 Diagrama Entidade-Relacionamento (ERD)

![ERD](diagrams/erd.png)

**Descrição:** O diagrama ERD representa o esquema do banco de dados, mostrando as entidades (modelos) e os relacionamentos entre elas.

### 🖥️ Diagrama de Arquitetura

![Arquitetura](diagrams/architecture.png)

**Descrição:** O diagrama de arquitetura ilustra os componentes principais do sistema e como eles interagem entre si, incluindo o cliente, API, banco de dados, cache, fila de tarefas e CI/CD.

## 📦 CI/CD

O projeto utiliza o **GitHub Actions** para integração contínua e entrega contínua (CI/CD). A cada push ou pull request nas branches `main` ou `master`, os testes automatizados são executados para garantir a integridade do código.

O workflow do GitHub Actions está definido no arquivo `.github/workflows/ci.yml`.

## 🐳 Comandos Úteis do Docker

- Para reiniciar o projeto: `docker-compose restart`
- Para parar os serviços: `docker-compose down`
- Para acessar o contêiner do Django: `docker-compose exec web bash`

## 📧 Suporte

Para qualquer dúvida ou problema, entre em contato em [wendell.cmd@gmail.com](mailto:wendell.cmd@gmail.com).

## 👤 Autor

- **Wendell Araújo** - [LinkedIn](https://www.linkedin.com/in/wendelloaraujo/) - wendell.cmd@gmail.com

---