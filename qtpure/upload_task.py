import os
from threading import Lock
from typing import Callable, Any

import requests
from PyQt5.QtCore import QThread, pyqtSignal

API_URL = os.environ.get('API_URL', 'http://projectvoid.play.ai:8080')


def upload_film(path_to_file: str,
                progress_func: Callable[[float], Any] = None,
                finish_func: Callable[[int], Any] = None):
    # Отправить пост запрос на сервер localhost:8080/api/post_video с файлом
    # После отправки запроса на сервер, сервер должен вернуть нам id фильма
    # Вернуть id фильма
    if progress_func is not None:
        progress_func(0.0)
    try:
        request = requests.post(f'{API_URL}/api/post_video',
                                files={'file': open(path_to_file, 'rb')})
        film_id = request.json()['id']
    except ConnectionError:
        raise ConnectionError("Ошибка соединения")
    if film_id < 0:
        raise Exception("Неудачна загрузка")

    if finish_func is not None:
        finish_func(film_id)


class UploadTask(QThread):
    progress_changed_signal = pyqtSignal(float)
    finished_signal = pyqtSignal(int)

    def __init__(self, path_to_file, lock: Lock):
        super().__init__()
        self.path_to_file = path_to_file
        self.lock = lock

    def __del__(self):
        self.wait()

    def run(self):
        def c1(x):
            self.progress_changed_signal.emit(x)

        def c2(x):
            self.finished_signal.emit(x)

        try:
            upload_film(self.path_to_file, c1, c2)
        except ConnectionError as e:
            print(e)
            c2(-2)
        except Exception as e:
            print(e)
            c2(-1)
