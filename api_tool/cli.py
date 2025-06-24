import argparse
import json
from typing import Optional
from . import RestApiTool, ApiError


def main():
    parser = argparse.ArgumentParser(description='REST API Tool CLI')

    # Основные параметры
    parser.add_argument('url', help='Base API URL')
    parser.add_argument('method', choices=['get', 'post', 'put', 'delete'], help='HTTP method')
    parser.add_argument('endpoint', help='API endpoint')

    # Опциональные параметры
    parser.add_argument('--token', help='Authorization token')
    parser.add_argument('--data', help='Request data (JSON string or file path)')
    parser.add_argument('--headers', help='Additional headers (JSON string)')
    parser.add_argument('--log-file', help='Path to log file')

    args = parser.parse_args()

    try:
        # Инициализация клиента
        api = RestApiTool(
            base_url=args.url,
            token=args.token,
            enable_file_logging=bool(args.log_file),
            log_file_path=args.log_file or "api_tool.log"
        )

        # Парсинг данных запроса
        data: Optional[dict] = None
        if args.data:
            try:
                # Попытка прочитать как JSON
                data = json.loads(args.data)
            except json.JSONDecodeError:
                # Попытка прочитать как файл
                try:
                    with open(args.data, 'r') as f:
                        data = json.load(f)
                except Exception as e:
                    print(f"Error reading data: {e}")
                    return

        # Парсинг заголовков
        headers: Optional[dict] = None
        if args.headers:
            try:
                headers = json.loads(args.headers)
            except json.JSONDecodeError as e:
                print(f"Invalid headers format: {e}")
                return

        # Выполнение запроса
        response = getattr(api, args.method)(
            endpoint=args.endpoint,
            data=data,
            headers=headers
        )

        # Вывод результата
        print(json.dumps(response, indent=2))

    except ApiError as e:
        print(f"API Error: {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
