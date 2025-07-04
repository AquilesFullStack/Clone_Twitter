# Backend Clone do Twitter

Este é o backend para uma aplicação clone do Twitter, desenvolvida com Django e Django REST Framework. A aplicação é totalmente containerizada usando Docker e Docker Compose para facilitar a configuração e o desenvolvimento.

## ✨ Features

-   **Autenticação de Usuário:** Sistema completo de registro, login e autenticação via `JWT (JSON Web Tokens)`.
-   **Gerenciamento de Usuários:** Criação, visualização e atualização de perfis de usuário.
-   **Envio de E-mail:** Confirmação de e-mail no registro de novos usuários.
-   **Postagens:** Funcionalidade de CRUD (Criar, Ler, Atualizar, Deletar) para postagens.
-   **Documentação da API:** Geração automática de documentação interativa com `Swagger (drf-yasg)`.
-   **Ambiente Isolado:** Configuração pronta para rodar com Docker, garantindo consistência entre ambientes.

## 🛠️ Tecnologias Utilizadas

-   **Backend:** Python, Django, Django REST Framework
-   **Banco de Dados:** PostgreSQL
-   **Servidor WSGI:** Gunicorn
-   **Containerização:** Docker, Docker Compose
-   **Outras bibliotecas:** `djangorestframework-simplejwt`, `drf-yasg`, `django-cors-headers`, `python-dotenv`

## 🚀 Como Rodar o Projeto

Siga os passos abaixo para configurar e rodar o ambiente de desenvolvimento localmente.

### Pré-requisitos

-   Docker
-   Docker Compose

### Passos de Instalação

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd twitter
    ```

2.  **Crie o arquivo de ambiente:**
    Copie o arquivo de exemplo `.env.example` para um novo arquivo chamado `.env`.
    ```bash
    # No Windows (cmd)
    copy .env.example .env

    # No Linux/macOS ou Windows (PowerShell)
    cp .env.example .env
    ```
    Em seguida, abra o arquivo `.env` e preencha as variáveis com seus valores, principalmente as credenciais de e-mail.

3.  **Construa e inicie os containers:**
    Este comando irá baixar as imagens necessárias, construir a imagem da sua aplicação e iniciar os serviços de backend e banco de dados.
    ```bash
    docker-compose up --build -d
    ```
    A flag `-d` executa os containers em segundo plano.

4.  **Execute as migrações do banco de dados:**
    Com os containers rodando, aplique as migrações do Django para criar as tabelas no banco de dados.
    ```bash
    docker-compose exec web python manage.py migrate
    ```

5.  **Crie um superusuário (opcional):**
    Para acessar a área administrativa do Django (`/admin`), crie um superusuário.
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

## 🌐 Acessando a Aplicação

-   **API:** `http://localhost:8000/`
-   **Documentação Swagger:** `http://localhost:8000/swagger/`
-   **Documentação Redoc:** `http://localhost:8000/redoc/`
-   **Admin Django:** `http://localhost:8000/admin/`

## 🛑 Parando os Containers

Para parar a aplicação, execute:
```bash
docker-compose down
```