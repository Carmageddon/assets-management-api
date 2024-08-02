# Assets Management API
Portfolio project showcasing what I can do with Python and Flask for API design
This is a Flask-based API for managing assets, including grouping assets based on user-defined rules. The application uses MongoDB for data storage.

## Features

- Add and manage assets
- Define and apply grouping rules for assets
- Automatically group assets based on rules

## Requirements

- Docker
- Docker Compose

## Development Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/assets-management-api.git
cd assets-management-api
```

### 2. Build the Docker image

```bash
docker-compose build
```

### 3. Run the Docker containers
```bash
docker-compose up -d
```
### 4. Access the application
Swagger REST API documentation should be accessible on `http://localhost:5000`

### 5 Run Tests
```bash
docker-compose -f docker-compose.test.yml build
docker-compose -f docker-compose.test.yml up --abort-on-container-exit --exit-code-from test
```


## Configuration

### MongoDB URI
The MongoDB URI can be configured using the MONGO_URI environment variable. The default URI is `mongodb://mongo:27017/myDatabase`.

## Production Setup

### 1. Set the MONGO_URI environment variable
In your production environment, set the MONGO_URI environment variable to point to your remote MongoDB server:
```bash
export MONGO_URI=mongodb://username:password@remote-mongo-server:27017/productionDatabase
```
### 2. Build and run the Docker image
```bash
docker-compose build
docker-compose up
```

## Project Structure

use `tree -I '.git|venv'` to regenerate the following:
```bash
.
├── Dockerfile
├── Dockerfile.dev
├── Dockerfile.prod
├── README.md
├── app
│   ├── __init__.py
│   ├── api.py
│   ├── assets
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── routes.py
│   ├── config.py
│   ├── main.py
│   ├── owners
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── utils.py
│   ├── rules
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── utils.py
│   └── utils.py
├── docker-compose.prod.yml
├── docker-compose.test.yml
├── docker-compose.yml
├── populate_assets.py
├── pytest.ini
├── requirements-dev.txt
├── requirements.txt
└── tests
    ├── conftest.py
    ├── test_assets.py
    ├── test_rules.py
    └── test_rules_utils.py
```