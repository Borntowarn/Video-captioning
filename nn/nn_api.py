import os

import flask

from inference import *

app = flask.Flask(__name__)
# cors
from flask_cors import CORS

CORS(app)


@app.route('/api', methods=['POST'])
def api():
    """
    Получение файла.
    Копирование его в inference_videos.
    Запуск inference main.py.
    Возврат файла из папки films_with_audiodescr с тем же названием, что и до обработки.
    """
    root_path = 'inference_videos'
    videos_path = 'clips'
    # получение файла
    file = flask.request.files['file']
    if file is None or file.filename == '':
        return 'No selected file', 405
    try:
        # копирование в inference_videos
        with open(os.path.join('inference_videos', file.filename), 'wb') as f:
            f.write(file.read())
        # запуск inference
        main(root_path, videos_path)
        # возврат файла
        return flask.send_from_directory('films_with_audiodescr', file.filename)
    except Exception as e:
        return str(e), 500
    finally:
        delete_files(root_path)
