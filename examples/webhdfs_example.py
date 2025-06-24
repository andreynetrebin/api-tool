from api_tool import RestApiTool
import json


class WebHDFSClient:
    def __init__(self, host: str, port: int = 50070, user: str = "hadoop"):
        self.api = RestApiTool(f"http://{host}:{port}/webhdfs/v1")
        self.user = user

    def _params(self, operation: str, **kwargs) -> dict:
        params = {"op": operation, "user.name": self.user}
        params.update(kwargs)
        return params

    def list_files(self, path: str) -> dict:
        """Получить список файлов в директории"""
        return self.api.get(path, params=self._params("LISTSTATUS"))

    def read_file(self, path: str) -> bytes:
        """Чтение файла"""
        return self.api.get(path, params=self._params("OPEN"))

    def upload_file(self, hdfs_path: str, local_path: str) -> bool:
        """Загрузка файла на HDFS"""
        # 1. Получаем URL для записи
        response = self.api.put(
            hdfs_path,
            params=self._params("CREATE", overwrite="true"),
            headers={"Content-Type": "application/octet-stream"}
        )

        # 2. Загружаем данные
        if 'Location' in response:
            with open(local_path, 'rb') as f:
                upload_url = response['Location']
                self.api.put("", full_url=upload_url, data=f.read())
                return True
        return False


# Пример использования
if __name__ == "__main__":
    client = WebHDFSClient("namenode", user="hadoop-user")

    # Список файлов
    files = client.list_files("/user/hadoop-user")
    print("Files:", json.dumps(files, indent=2))

    # Загрузка файла
    if client.upload_file("/user/hadoop-user/test.txt", "local.txt"):
        print("File uploaded successfully")

    # Чтение файла
    content = client.read_file("/user/hadoop-user/test.txt")
    print("File content:", content[:100])
