# REST API Tool

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Библиотека на Python для работы с REST API. Поддерживает аутентификацию, операции с файлами и предоставляет детализированное логирование.

## Возможности

- Поддержка всех HTTP методов (GET, POST, PUT, PATCH, DELETE)
- Загрузка/скачивание файлов
- Гибкая аутентификация (Bearer, Basic, API ключи)
- Подробное логирование в консоль/файл
- Комплексная обработка ошибок
- Поддержка аннотаций типов

## Установка

```bash
pip install api-tool
```

## Быстрый старт

```python
from api_tool import RestApiTool

# Инициализация клиента
api = RestApiTool("https://api.example.com", token="ваш_токен")

# GET запрос
response = api.get("/users")

# POST запрос
new_user = api.post("/users", data={"name": "Иван"})
```

## Документация

Полная документация доступна в [папке docs](docs/quickstart.md).
