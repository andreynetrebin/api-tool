# Быстрый старт с REST API Tool

## Установка

### Установка из локального каталога

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/andreynetrebin/api-tool.git
   cd api-tool
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Установите пакет:
   ```bash
   pip install .
   ```

### Установка из GitHub

Вы можете установить пакет напрямую из GitHub:

```bash
pip install git+https://github.com/andreynetrebin/api-tool.git
```

### Установка из ZIP-архива

1. Скачайте ZIP-архив с [GitHub](https://github.com/yourusername/api-tool/archive/refs/heads/main.zip).
2. Распакуйте архив и перейдите в каталог проекта:
   ```bash
   unzip api-tool-main.zip
   cd api-tool-main
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Установите пакет:
   ```bash
   pip install .
   ```

## Базовое использование

### Инициализация клиента

```python
from api_tool import RestApiTool

# Без аутентификации
api = RestApiTool("https://api.example.com")

# С токеном аутентификации
api = RestApiTool("https://api.example.com", token="ваш_токен")
```

### Примеры запросов

GET запрос:
```python
response = api.get("/users")
print(response)
```

POST запрос с данными:
```python
data = {"name": "John", "email": "john@example.com"}
response = api.post("/users", data=data)
```

Загрузка файла:
```python
api.upload_file("/uploads", "local_file.txt")
```

## Логирование

```python
# Логирование в файл
api = RestApiTool(
    "https://api.example.com",
    enable_file_logging=True,
    log_file_path="api.log"
)
```

## Обработка ошибок

```python
try:
    response = api.get("/protected")
except ApiError as e:
    print(f"Ошибка API: {e}")
```

## CLI интерфейс

Пример использования через командную строку:

```bash
python -m api_tool.cli https://api.example.com get /users --token "ваш_токен"
```