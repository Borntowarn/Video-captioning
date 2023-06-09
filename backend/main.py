import os
import re
import shutil
import traceback
from datetime import datetime
from pathlib import Path
from threading import Lock, Thread
from time import sleep
from typing import Callable, Any, Iterable, Mapping, Union

import moviepy.editor as mp
import requests
from flask import Flask, request, Response, send_file
from flask_cors import CORS

from model.film import Film, Session, clear

app = Flask(__name__)
CORS(app)

API_NN_URL = os.environ.get('API_NN_URL', "http://localhost:8081")

session = Session()


@app.route('/api/await_url_updated_video', methods=['GET'], strict_slashes=False)
def wait_and_get_url_to_updated_video():
    # Ожидание появления обновленного видео с интервалом в секунду, но не более минуты
    # После появления видео, вернуть ссылку на него
    # Если видео не появилось, вернуть None
    film_id = request.args.get('film_id')
    if film_id is None:
        # Вернуть BAD REQUEST
        return "Не указан film_id", 400
    film = session.query(Film).filter(Film.id == film_id).first()
    if film is None:
        return {"url": None}
    time_start = datetime.now()
    while film.output_video_filename is None:
        sleep(1)
        film = session.query(Film).filter(Film.id == film_id).first()
        time_now = datetime.now()
        if (time_now - time_start).seconds > 60:
            return {"url": None}
    return {"url": f"{API_NN_URL}/api/get_video?film_id={film_id}&only_updated=1"}


@app.route('/api/await_and_get_updated_video', methods=['GET'], strict_slashes=False)
def await_and_get_updated_video():
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
    return {"url": f"{API_NN_URL}/api/get_video?film_id={film_id}&only_updated=1"}


file_lock = Lock()


class ProcessPipe(Thread):

    def __init__(self, group: None = None,
                 target: Union[Callable[..., Any], None] = None,
                 name: Union[str, None] = None,
                 args: Iterable[Any] = None,
                 kwargs: Union[Mapping[str, Any], None] = None,
                 *,
                 daemon: Union[bool, None] = None) -> None:
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

    def recycle(self, path: str) -> Union[bytes, None]:
        # Отправить файл на обработку в нейросеть через NN_API_URL/api POST
        r = requests.post(f"{API_NN_URL}/api",
                          files={"file": open(path, 'rb')})
        # Получить ответ в виде файла и сохранить его с тем же именем,
        # что и входной файл, но с добавкой "_updated"
        # Проверка наличия в ответе файла
        if r.status_code != 200:
            return
        if r.headers['Content-Type'] != 'video/mp4':
            return
        return r.content

    def iterate_process(self):
        if not os.path.exists('data/tmp'):
            os.mkdir('data/tmp')
        if len(self.films_in_process) < 1:
            return
        for film in self.films_in_process.copy():
            with self.lock:
                self.films_in_process.remove(film)
            if film.output_video_filename is not None:
                # Удалить файл и убрать запись об обработке
                film.output_video_filename = None
                session.commit()
            film_filename = film.input_filename
            updated_film_filename = f"{Path(film_filename).stem}_updated{Path(film_filename).suffix}"
            updated_film_path = os.path.join('data', 'films', updated_film_filename)
            if os.path.exists(updated_film_path):
                os.remove(updated_film_path)
            if not os.path.exists(os.path.join('data', 'films', film_filename)):
                continue
            # Разделить видео по 10 минут
            print(f"Делим на куски фильм {film_filename}")
            input_clip = mp.VideoFileClip(os.path.join('data', 'films', film_filename))
            clips: list[mp.VideoFileClip] = []
            first_clip_durations = [60, 300, 600]
            step = 0
            cur_time = 0
            end_time = 0
            while end_time < int(input_clip.duration):
                # Не допускаем уходить в бесконечность
                if first_clip_durations[step] > 0:
                    end_time += first_clip_durations[step]
                else:
                    end_time += 600
                if end_time > input_clip.duration:
                    end_time = input_clip.duration
                clips.append(input_clip.subclip(cur_time, end_time))
                print(f"Кусок {end_time - cur_time} секунд")
                cur_time = end_time
                if step < len(first_clip_durations) - 1:
                    step += 1

            # Отправить каждый кусок на обработку
            broken_film = False
            for i, clip in enumerate(clips):
                clip_filename = f"{Path(film_filename).stem}_{i}{Path(film_filename).suffix}"
                clip_path = os.path.join('data', 'tmp', clip_filename)
                clip.write_videofile(clip_path,
                                     codec='libx264' if 'mkv' in Path(film_filename).suffix else None)
                print(f"Кусок {i} сохранен в {clip_path}")
                updated_clip_content = self.recycle(clip_path)
                if updated_clip_content is None:
                    broken_film = True
                    break
                # Сохраняет полученный кусок в файл с суффиксом "_updated"
                updated_clip_filename = f"{Path(film_filename).stem}_{i}_updated{Path(film_filename).suffix}"
                updated_clip_path = os.path.join('data', 'tmp', updated_clip_filename)
                print(f"Сохраняем обновленный кусок в файл {updated_clip_path}")
                with open(updated_clip_path, 'wb') as f:
                    f.write(updated_clip_content)
                # Склеивание с текущим обработанным фильмом
                copy_updated_film_path = None
                if not os.path.exists(os.path.join(updated_film_path)):
                    new_updated_film = mp.VideoFileClip(updated_clip_path)
                else:
                    copy_updated_film_filename = f"{Path(updated_film_path).stem}_updated{Path(updated_film_path).suffix}"
                    copy_updated_film_path = os.path.join('data/tmp', copy_updated_film_filename)
                    shutil.copy(updated_film_path, copy_updated_film_path)
                    new_updated_film = mp.concatenate_videoclips([
                        mp.VideoFileClip(copy_updated_film_path),
                        mp.VideoFileClip(updated_clip_path)]
                    )

                new_updated_film_filename = f"{Path(film_filename).stem}_updated_new{Path(film_filename).suffix}"
                new_updated_film_path = os.path.join('data/tmp', new_updated_film_filename)
                new_updated_film.write_videofile(new_updated_film_path,
                                                 codec='libx264' if 'mkv' in Path(
                                                     new_updated_film_path).suffix else None)

                print(f"Фильм дополнен до {new_updated_film.duration} секунд")
                with file_lock:
                    shutil.copy(new_updated_film_path, updated_film_path)
                os.remove(new_updated_film_path)
                film = session.query(Film).filter(Film.id == film.id).first()
                film.output_video_filename = updated_film_filename
                session.commit()
                # Удалить временные файлы
                try:
                    new_updated_film.close()
                    if os.path.exists(clip_path):
                        os.remove(clip_path)
                    if os.path.exists(updated_clip_path):
                        os.remove(updated_clip_path)
                    if copy_updated_film_path is not None:
                        if os.path.exists(copy_updated_film_path):
                            os.remove(copy_updated_film_path)
                except Exception as _:
                    pass
            input_clip.close()
            if broken_film:
                # TODO: Сохранить фильм в базу данных как "broken"
                continue


pipe = ProcessPipe()
pipe.start()


# Получение видео в запросе
@app.route('/api/post_video', methods=['POST'], strict_slashes=False)
def handle_request():
    try:
        # Получение файла из запроса
        if 'file' not in request.files:
            return "File not set", 400
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
        traceback.print_exception(e)
        return {"id": -1}, 500


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
