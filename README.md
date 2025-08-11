# REST API Tool

![api_tool](https://github.com/user-attachments/assets/01787247-a11c-4a97-b347-ac6def6b4b3f)

Библиотека на Python для работы с REST API. Поддерживает аутентификацию, операции с файлами и предоставляет детализированное логирование.

## Содержание

- [Возможности](#возможности)
- [Установка](#установка)
- [Документация](#документация)
- [Лицензия](#лицензия)

## Возможности

- Поддержка всех HTTP методов (GET, POST, PUT, PATCH, DELETE)
- Загрузка/скачивание файлов
- Гибкая аутентификация (Bearer, Basic, API ключи)
- Подробное логирование в консоль/файл
- Комплексная обработка ошибок
- Поддержка аннотаций типов

## Установка


### Установка из локального каталога
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/andreynetrebin/api-tool.git
   cd api-tool

2. Установите зависимости:
    ```bash
    pip install -r requirements.txt

3. Установите пакет:
    ```bash
    pip install .

### Установка из GitHub
1. Вы можете установить пакет напрямую из GitHub:
    ```bash
    pip install git+https://github.com/andreynetrebin/api-tool.git

### Установка из ZIP-архива
1. Скачайте ZIP-архив с GitHub.
2. Распакуйте архив и перейдите в каталог проекта:
    ```bash
    unzip api-tool-main.zip
    cd api-tool-main
3. Установите зависимости:
    ```bash
    pip install -r requirements.txt
4. Установите зависимости:
    ```bash
    pip install .

## Документация

Полная документация доступна в [папке docs](docs/quickstart.md).

## Лицензия

Этот проект лицензирован под лицензией MIT.
