import shutil
from pathlib import Path

import flask
from flask import request
from flask_cors import CORS

from inference import *

app = flask.Flask(__name__)
CORS(app)

def just_copy(filename):
    """
    Просто копирует файл из папки inference_videos/videos в папку films_with_audiodescr
    """
    input_path = 'inference_videos'
    output_path = 'films_with_audiodescr'
    videos_path = input_path + '/' + 'videos'
    final_film_path = os.path.join(output_path, filename)
    shutil.copy(os.path.join(videos_path, filename), final_film_path)

@app.route('/api', methods=['POST'], strict_slashes=False)
def api():
    """
    Получение файла.
    Копирование его в inference_videos.
    Запуск inference main.py.
    Возврат файла из папки films_with_audiodescr с тем же названием, что и до обработки.
    """
    input_path = 'inference_videos'
    clips_folder = 'clips'
    clips_path = input_path + '/' + clips_folder
    videos_path = input_path + '/' + 'videos'
    output_path = 'films_with_audiodescr'

    # Проверка наличия папки inference_videos
    if not os.path.exists(input_path):
        os.makedirs(input_path)
    # Проверка наличия папки clips внутри inference_videos
    if not os.path.exists(clips_path):
        os.makedirs(clips_path)
    # получение файла
    if 'file' not in request.files:
        return 'No file part', 405
    file = flask.request.files['file']
    if file is None or file.filename == '':
        return 'No selected file', 405
    try:
        temp_filename = 'temp' + Path(file.filename).suffix
        # копирование в inference_videos
        file.save(os.path.join(videos_path, temp_filename))
        # запуск inference
        # main(input_path, clips_folder)
        # Получение обработанного видео
        final_film_path = os.path.join(output_path, temp_filename)
        # возврат файла
        return flask.send_file(final_film_path, as_attachment=True)
    except Exception as e:
        return str(e), 500
    finally:
        delete_files(input_path)


if __name__ == '__main__':
    # get port from sys env PORT or default
    port = int(os.environ.get('PORT', 8081))
    print(f"Starting API server on port {port}...")
    app.run(host='0.0.0.0', port=port)
