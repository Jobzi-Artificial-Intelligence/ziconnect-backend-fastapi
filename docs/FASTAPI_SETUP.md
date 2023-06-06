# Jobzi School Connectivity

## Setting up the local environment for the backend side

This guide explains how to set up your local environment. It includes information about prerequisites, installation, build and running that app locally to verify your setup.

## Requirements

### Preconditions

- Docker
- Python3

### Clone FastApi Project 

```
git clone https://github.com/tiangolo/fastapi
```

### Run local 

#### Install dependencies

```
pip install -r requirements.txt
```

#### Run server

```
uvicorn app.main:app --reload
```

#### Run test

```
pytest fastapi/tests/test_main.py
```

### Run with docker

#### Run server

```
docker-compose up -d --build
```

#### Run test

```
docker-compose exec fastapi pytest fastapi/tests/test_main.py
```

## API documentation (provided by Swagger UI)

```
http://127.0.0.1:8000/docs
```


## Run Development server

Run `` for a dev server. Navigate to `http://localhost:8000/`. The app will automatically reload if you change any of the source files.

```
http://127.0.0.1:8000
```

## Interact with the FastAPI

After running development server, accessing the address .

In this project, we used the open source .

## Interact with the Celery and Flower Dashboard

After running development server, accessing the.

## Build the project

Run  to build the project. 

## Visual Studio Code

Is a source-code editor made by Microsoft with the Electron Framework, for Windows, Linux and macOS. Features include support for debugging, syntax highlighting, intelligent code completion, snippets, code refactoring, and embedded Git.

These are some of the extensions that help in the development process of this project:

- [Angular Snippets](https://marketplace.visualstudio.com/items?itemName=johnpapa.Angular2): This extension for Visual Studio Code adds snippets for Angular for TypeScript and HTML.
- [Prettier](https://prettier.io/): is an opinionated code formatter. It enforces a consistent style by parsing your code and re-printing it with its own rules that take the maximum line length into account, wrapping code when necessary.
- [ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint): Integrates ESLint into VS Code
