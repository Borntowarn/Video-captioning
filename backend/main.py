import os
import re
from datetime import datetime
from pathlib import Path
from threading import Lock, Thread
from time import sleep
from typing import Callable, Any, Iterable, Mapping

import moviepy.editor as mp
import requests
from flask import Flask, request, Response, send_file
from flask_cors import CORS

from model.film import Film, Session

app = Flask(__name__)
CORS(app)

NN_API_URL = "http://localhost:8081"

@app.route('/api/await_url_updated_video', methods=['GET'], strict_slashes=False)
def wait_and_get_url_to_updated_video():
    # Ожидание появления обновленного видео с интервалом в секунду, но не более минуты
    # После появления видео, вернуть ссылку на него
    # Если видео не появилось, вернуть None
    session = Session()
    film_id = request.args.get('film_id')
    if film_id is None:
        # Вернуть BAD REQUEST
        return "Не указан film_id", 400
    film = session.query(Film).filter(Film.id == film_id).first()
    if film is None:
        return {"url": None}
    time_start = datetime.now()
    while film.output_video_filename is None:
        film = session.query(Film).filter(Film.id == film_id).first()
        time_now = datetime.now()
        if (time_now - time_start).seconds > 60:
            return {"url": None}
    return {"url": f"{NN_API_URL}/api/get_video?film_id={film_id}&only_updated=1"}


class ProcessPipe(Thread):

    def __init__(self, group: None = None,
                 target: Callable[..., Any] | None = None,
                 name: str | None = None,
                 args: Iterable[Any] = None,
                 kwargs: Mapping[str, Any] | None = None,
                 *,
                 daemon: bool | None = None) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.lock = Lock()
        self.films_to_process: list[Film] = []
        self.films_in_process: list[Film] = []
        self.is_running = False

    def run(self) -> None:
        while True:
            if len(self.films_to_process) < 1:
                sleep(1)
                continue
            with self.lock:
                self.films_in_process = self.films_to_process[:1]
                self.films_to_process = self.films_to_process[1:]
            self.iterate_process()

    def add_film_to_processing(self, film: Film):
        with self.lock:
            if film not in self.films_to_process:
                self.films_to_process.append(film)

    def iterate_process(self):
        if len(self.films_in_process) < 1:
            return
        for film in self.films_in_process.copy():
            with self.lock:
                self.films_in_process.remove(film)
            path = film.input_filename
            if not os.path.exists(os.path.join('data', 'films', path)):
                continue
            # Отправить файл на обработку в нейросеть через NN_API_URL/api POST
            r = requests.post(f"{NN_API_URL}/api",
                              files={"file": open(os.path.join('data', 'films', path), 'rb')})
            # Получить ответ в виде файла и сохранить его с тем же именем,
            # что и входной файл, но с добавкой "_updated"
            # Проверка наличия в ответе файла
            if r.status_code != 200:
                continue
            if r.headers['Content-Type'] != 'video/mp4':
                continue
            filename_out = Path(path).stem + '_updated' + Path(path).suffix
            with open(os.path.join('data', 'films', filename_out), 'wb') as f:
                f.write(r.content)
            # Обновить запись в бд
            with Session() as session:
                film = session.query(Film).filter(Film.id == film.id).first()
                film.output_video_filename = filename_out
                session.commit()
                session.flush()
            pass


pipe = ProcessPipe()
pipe.start()


# Получение видео в запросе
@app.route('/api/post_video', methods=['POST'], strict_slashes=False)
def handle_request():
    session = Session()
    try:
        # Получение файла из запроса
        file = request.files['file']
        file_content = file.read()
        # Сохранение файла в бд
        film = Film(name=file.filename.split('.')[0], hash=len(file_content), input_filename=file.filename,
                    output_video_filename=None)
        # Проверка наличия двойника
        found_film = session.query(Film).filter(Film.hash == film.hash).first()
        if found_film is not None:
            return {"id": found_film.id}
        session.add(film)
        session.commit()

        # Создание папки data/films
        if not os.path.exists(os.path.join('data', 'films')):
            os.makedirs(os.path.join('data', 'films'))
        # Сохранение файла на data/films
        with open(os.path.join('data', 'films', file.filename), 'wb') as f:
            f.write(file_content)
        # Отправка файла на обработку
        pipe.add_film_to_processing(film)
        pipe.join(0.02)

        # Возвращение id фильма
        return {"id": film.id}
    except Exception as e:
        print(e)
        return {"id": -1}
    finally:
        session.close()


def video_length(path):
    duration = mp.VideoFileClip(path).duration
    return duration


@app.route('/api/get_video/', methods=['GET'], strict_slashes=False)
def get_video():
    session = Session()
    try:
        film_id = request.args.get('film_id')
        film = session.query(Film).filter(Film.id == film_id).first()
        only_updated = request.args.get('only_updated', 'false').lower() in ['true', '1']
        metadata = request.args.get('metadata', 'false').lower() in ['true', '1']
        if film is None:
            return {"status": "error", "message": "Фильм не найден"}
        if only_updated:
            if film.output_video_filename is None:
                return Response("Фильм еще не обработан")
            path = os.path.join('data', 'films', film.output_video_filename)
            if metadata:
                return {"length": video_length(path)}
            return send_file(path)
        path = os.path.join('data', 'films', film.input_filename)
        if metadata:
            return {"length": video_length(path)}
        return send_file(path)

    except Exception as e:
        print(e)
        return {"status": "error", "message": "Неизвестная ошибка"}
    finally:
        session.close()


if __name__ == '__main__':
    # get port from sys env PORT or default to 8080
    port = int(os.environ.get('PORT', 8080))
    print(f"Starting API server on port {port}...")
    app.run(host='0.0.0.0', port=port)
