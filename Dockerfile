#Versão do Python base
FROM python:3.12.7-slim

# diretório de trabalho
WORKDIR /app

# Dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Copiar o script wait-for-it
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Copiar os requisitos
COPY requirements.txt .

# Dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código do projeto
COPY . .

# Expor a porta 8000
EXPOSE 8000

# iniciar o servidor Django, usando o script wait-for-it para garantir que o servidor só inicie quando o banco de dados estiver pronto.
CMD ["/wait-for-it.sh", "db:5432", "--", "python", "manage.py", "runserver", "0.0.0.0:8000"]
