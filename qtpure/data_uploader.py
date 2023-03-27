import requests
from PyQt5.QtCore import QThread
from PySide2.QtCore import Signal

API_URL = "http://localhost:8080"


class DataUploader(QThread):
    progress_signal = Signal(float)
    finish_signal = Signal(int)

    def __init__(self, path_to_file=None):
        super(DataUploader, self).__init__()
        self.path_to_file = path_to_file

    def run(self):
        # Отправить пост запрос на сервер localhost:8080/api/post_video с файлом
        # После отправки запроса на сервер, сервер должен вернуть нам id фильма
        # Вернуть id фильма

        DataUploader.progress_signal.emit(0.0)
        request = requests.post(f'{API_URL}/api/post_video',
                                files={'file': open(self.path_to_file, 'rb')})
        film_id = request.json()['id']
        if film_id < 0:
            raise Exception("Неудачна загрузка")
        DataUploader.finish_signal.emit(film_id)
