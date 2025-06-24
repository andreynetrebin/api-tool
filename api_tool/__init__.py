"""
REST API Tool - Python library for working with REST APIs

Features:
- Supports all HTTP methods (GET, POST, PUT, PATCH, DELETE)
- File uploads/downloads
- Flexible authentication
- Detailed logging
- Error handling
"""

import requests
import logging
from typing import Optional, Union, Dict, Any
import os
from datetime import datetime

__version__ = "1.0.0"

class ApiError(Exception):
    """Custom exception for API errors"""
    pass

class RestApiTool:
    def __init__(self, base_url: str, token: Optional[str] = None,
                 enable_file_logging: bool = False, log_file_path: str = "api_tool.log"):
        """Initialize API client"""
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.session = requests.Session()
        self._setup_logging(enable_file_logging, log_file_path)

    def _setup_logging(self, enable_file_logging: bool, log_file_path: str):
        """Настройка логирования"""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Очистка предыдущих обработчиков
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

        # Формат логов
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Обработчик для консоли
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Обработчик для файла (если включено)
        if enable_file_logging:
            try:
                # Создаем директорию для логов если ее нет
                os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

                file_handler = logging.FileHandler(log_file_path)
                file_handler.setLevel(logging.DEBUG)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)

                self.logger.info(f"Логирование настроено в файл: {log_file_path}")
            except Exception as e:
                self.logger.error(f"Ошибка настройки файлового логирования: {str(e)}")

    def set_token(self, token: str):
        """Установить токен для аутентификации"""
        self.token = token
        self.logger.info("Токен установлен")

    def _get_headers(self, custom_headers: Optional[Dict] = None) -> Dict:
        """
        Формирование заголовков запроса

        :param custom_headers: Дополнительные заголовки
        :return: Словарь с заголовками
        """
        headers = {'Accept': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        if custom_headers:
            headers.update(custom_headers)
        return headers

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """
        Базовый метод для выполнения HTTP запросов

        :param method: HTTP метод (GET, POST и т.д.)
        :param endpoint: Конечная точка API
        :param kwargs: Дополнительные параметры для requests
        :return: Объект Response
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self._get_headers(kwargs.pop('headers', None))

        self.logger.info(f"Отправка {method} запроса на {url}")
        try:
            response = self.session.request(method, url, headers=headers, **kwargs)

            self.logger.info(f"Получен ответ: {response.status_code}")
            self.logger.debug(f"Заголовки запроса: {response.request.headers}")

            if 'data' in kwargs:
                self.logger.debug(f"Тело запроса: {str(kwargs['data'])[:500]}")
            elif 'json' in kwargs:
                self.logger.debug(f"JSON тело: {str(kwargs['json'])[:500]}")

            self.logger.debug(f"Тело ответа: {response.text[:500]}...")

            return response

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Ошибка при выполнении запроса: {str(e)}")
            raise ApiError(f"Ошибка сети: {str(e)}")

    def _handle_response(self, response: requests.Response) -> Union[Dict, str]:
        """
        Обработка ответа от сервера

        :param response: Объект Response
        :return: Распарсенные данные или текст ответа
        :raises ApiError: Если статус код не 2xx
        """
        try:
            if response.status_code in range(200, 300):
                try:
                    return response.json()
                except ValueError:
                    return response.text
            else:
                error_msg = f"Ошибка {response.status_code}: {response.text}"
                self.logger.error(error_msg)
                raise ApiError(error_msg)
        except Exception as e:
            self.logger.error(f"Ошибка обработки ответа: {str(e)}")
            raise ApiError(f"Ошибка обработки ответа: {str(e)}")

    # Все методы запросов остаются без изменений (get, post, put и т.д.)
    # ... (остальные методы остаются такими же как в предыдущей версии)

    def get(self, endpoint: str, params: Optional[Dict] = None, headers: Optional[Dict] = None, **kwargs) -> Union[
        Dict, str]:
        """
        GET запрос

        :param endpoint: Конечная точка API
        :param params: Параметры запроса
        :param headers: Дополнительные заголовки
        :param kwargs: Дополнительные параметры для requests
        :return: Ответ сервера
        """
        response = self._make_request('GET', endpoint, params=params, headers=headers, **kwargs)
        return self._handle_response(response)

    def post(self, endpoint: str, data: Optional[Any] = None, headers: Optional[Dict] = None, **kwargs) -> Union[
        Dict, str]:
        """
        POST запрос

        :param endpoint: Конечная точка API
        :param data: Данные для отправки
        :param headers: Дополнительные заголовки
        :param kwargs: Дополнительные параметры для requests
        :return: Ответ сервера
        """
        response = self._make_request('POST', endpoint, json=data, headers=headers, **kwargs)
        return self._handle_response(response)

    def post_form(self, endpoint: str, data: Optional[Dict] = None, headers: Optional[Dict] = None, **kwargs) -> Union[
        Dict, str]:
        """
        POST запрос с form-data

        :param endpoint: Конечная точка API
        :param data: Данные формы
        :param headers: Дополнительные заголовки
        :param kwargs: Дополнительные параметры для requests
        :return: Ответ сервера
        """
        response = self._make_request('POST', endpoint, data=data, headers=headers, **kwargs)
        return self._handle_response(response)

    def put(self, endpoint: str, data: Optional[Any] = None, headers: Optional[Dict] = None, **kwargs) -> Union[
        Dict, str]:
        """
        PUT запрос

        :param endpoint: Конечная точка API
        :param data: Данные для отправки
        :param headers: Дополнительные заголовки
        :param kwargs: Дополнительные параметры для requests
        :return: Ответ сервера
        """
        response = self._make_request('PUT', endpoint, json=data, headers=headers, **kwargs)
        return self._handle_response(response)

    def patch(self, endpoint: str, data: Optional[Any] = None, headers: Optional[Dict] = None, **kwargs) -> Union[
        Dict, str]:
        """
        PATCH запрос

        :param endpoint: Конечная точка API
        :param data: Данные для отправки
        :param headers: Дополнительные заголовки
        :param kwargs: Дополнительные параметры для requests
        :return: Ответ сервера
        """
        response = self._make_request('PATCH', endpoint, json=data, headers=headers, **kwargs)
        return self._handle_response(response)

    def delete(self, endpoint: str, headers: Optional[Dict] = None, **kwargs) -> Union[Dict, str]:
        """
        DELETE запрос

        :param endpoint: Конечная точка API
        :param headers: Дополнительные заголовки
        :param kwargs: Дополнительные параметры для requests
        :return: Ответ сервера
        """
        response = self._make_request('DELETE', endpoint, headers=headers, **kwargs)
        return self._handle_response(response)

    def upload_file(self, endpoint: str, file_path: str, field_name: str = 'file',
                    extra_data: Optional[Dict] = None, headers: Optional[Dict] = None) -> Union[Dict, str]:
        """
        Загрузка файла на сервер

        :param endpoint: Конечная точка API
        :param file_path: Путь к файлу
        :param field_name: Имя поля для файла
        :param extra_data: Дополнительные данные
        :param headers: Дополнительные заголовки
        :return: Ответ сервера
        """
        try:
            self.logger.info(f"Начало загрузки файла {file_path}")
            with open(file_path, 'rb') as f:
                files = {field_name: f}
                data = extra_data or {}
                response = self._make_request('POST', endpoint, files=files, data=data, headers=headers)
                self.logger.info(f"Файл {file_path} успешно загружен")
                return self._handle_response(response)
        except IOError as e:
            error_msg = f"Ошибка чтения файла {file_path}: {str(e)}"
            self.logger.error(error_msg)
            raise ApiError(error_msg)
