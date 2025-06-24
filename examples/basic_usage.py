"""
Примеры базового использования API Tool для работы с REST API
"""

from api_tool import RestApiTool, ApiError

def main():
    # 1. Инициализация клиента с базовым URL и токеном
    api = RestApiTool(
        base_url="https://jsonplaceholder.typicode.com",
        token="your_access_token_here",  # Опционально
        enable_file_logging=True,
        log_file_path="api_usage.log"
    )

    print("\n=== Пример 1: GET запрос ===")
    try:
        # Получение списка пользователей
        users = api.get("/users")
        print(f"Получено {len(users)} пользователей")
        print(f"Первый пользователь: {users[0]['name']}")
    except ApiError as e:
        print(f"Ошибка при получении пользователей: {e}")

    print("\n=== Пример 2: POST запрос ===")
    new_post = {
        "title": "Новый пост",
        "body": "Содержание нового поста",
        "userId": 1
    }
    try:
        created_post = api.post("/posts", data=new_post)
        print(f"Создан пост с ID: {created_post['id']}")
    except ApiError as e:
        print(f"Ошибка при создании поста: {e}")

    print("\n=== Пример 3: Работа с заголовками ===")
    custom_headers = {
        "X-Custom-Header": "MyValue",
        "Accept": "application/json"
    }
    try:
        response = api.get("/posts/1", headers=custom_headers)
        print(f"Получен пост: {response['title']}")
    except ApiError as e:
        print(f"Ошибка при получении поста: {e}")

    print("\n=== Пример 4: Обработка ошибок ===")
    try:
        # Несуществующий ресурс
        response = api.get("/non-existent-endpoint")
    except ApiError as e:
        print(f"Поймана ожидаемая ошибка: {e}")

if __name__ == "__main__":
    main()
