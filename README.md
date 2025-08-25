# Django Studies

Este projeto é um exemplo de aplicação Django para estudos.

## Pré-requisitos
- Python 3.12+
- Docker e Docker Compose (opcional, mas recomendado)
- Git

## Instalação

### 1. Clonar o repositório
```bash
git clone https://github.com/francescooviiedo/django-studies.git
cd django-studies
```

### 2. Criar e ativar o ambiente virtual (opcional, se não usar Docker)
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instalar as dependências
```bash
pip install -r requirements.txt
```

## Utilizando Docker (recomendado)

### 1. Construir e iniciar os containers
```bash
docker-compose up --build
```

### 2. Aplicar as migrações
```bash
docker-compose exec web python manage.py migrate
```

## Executando o projeto sem Docker

### 1. Aplicar as migrações
```bash
python manage.py migrate
```

### 2. Iniciar o servidor
```bash
python manage.py runserver
```

## Acessando a aplicação
Abra o navegador e acesse:
```
http://localhost:8000/
```

## Observações
- O arquivo `.env` pode ser usado para variáveis de ambiente (não versionado).
- O banco de dados padrão é SQLite, mas pode ser alterado em `settings.py`.

---

Sinta-se à vontade para contribuir ou abrir issues!
