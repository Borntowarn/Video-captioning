import http.client
import os
import re
from datetime import time, datetime

from flask import Flask, request, Response, send_file
from flask_cors import CORS
from model.film import Film, Session

app = Flask(__name__)
CORS(app)


def get_notifications_to_user(user_id):
    return [{"id": 1, "text": "Вы не закончили форму"},
            {"id": 2, "text": "Скоро закрывается форма для регистрации соревнования"}]


def union_article_and_url(article: str, url: str) -> str:
    return f"<a href='{url}' target='_blank'>{article}</a>"


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
    return {"url": f"http://localhost:8080/api/get_video?film_id={film_id}&only_updated=1"}


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

        # Возвращение id фильма
        return {"id": film.id}
    except Exception as e:
        print(e)
        return {"id": -1}
    finally:
        session.close()


@app.route('/api/get_video/', methods=['GET'], strict_slashes=False)
def get_video():
    session = Session()
    try:
        film_id = request.args.get('film_id')
        film = session.query(Film).filter(Film.id == film_id).first()
        only_updated = request.args.get('only_updated', 'false').lower() in ['true', '1']
        only_source = request.args.get('only_source', 'false').lower() in ['true', '1']
        if film is None:
            return {"status": "error", "message": "Фильм не найден"}
        if only_updated:
            if film.output_video_filename is None:
                return Response("Фильм еще не обработан")
            return send_file(os.path.join('data', 'films', film.output_video_filename))
        return send_file(os.path.join('data', 'films', film.input_filename))
    except Exception as e:
        print(e)
        return {"status": "error", "message": "Неизвестная ошибка"}
    finally:
        session.close()


def find_and_format_email(msg: str) -> str:
    # Regular expression pattern for matching email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    # Find all email addresses in the string using regex
    matches = re.findall(email_pattern, msg)

    # Replace each email address with the formatted version
    for match in matches:
        msg = msg.replace(match, f'<b>{match}</b>')

    return msg


@app.route('/api/voice', methods=['POST'])
def handle_request_audio():
    # get the data from the request
    audio = request.values.get('file')

    from_url = request.form.get('from_url')
    is_web = request.values.get('is_web', False)
    # process audio to text
    text = get_text(audio)

    # process the data (for example, send it to another server and get the response)
    result = web_bot(text)
    if is_web:
        result = find_and_format_email(result)
    return {"text": ' '.join(result[0])}
    # return the response to the bot
    return {"text": "Response from the API server", "buttons_text": ["Only", "One", "Word"]}


@app.route('/api/notifications', methods=['GET'])
def handle_request_notifications():
    from_url = request.form.get('from_url')
    # process audio to text
    user_id = request.form.get('user_id')

    return {"notifications": get_notifications_to_user(user_id)}


@app.route('/api/notifications/acknowledge', methods=['POST'])
def handle_request_acknowledge_notification():
    pass

    return http.client.OK


if __name__ == '__main__':
    # get port from sys env PORT or default to 8080
    port = int(os.environ.get('PORT', 8080))
    print(f"Starting API server on port {port}...")
    app.run(host='0.0.0.0', port=port)
