import json

import requests


class SpeechKitApi:
    def __init__(self, oauth_token, folder_id):
        self._oauth_token = oauth_token
        self.token = "t1.9euelZqKkM3Nip2Uys6ZkJjHipTKnu3rnpWakpySmIqOmpTOmJ6VmM-XzZPl8_dKVAJf-e8LMQVQ_N3z9woDA" \
                     "F_57wsxBVD8.s_k3nHOl23IYidjb9cFWf6LeZniMOV7yUc_cch-jAoVGfI8H2cpsKWAN74-pzpadRf82aohp" \
                     "mBzLFCVqLbpDAg"
        self.folder_id = folder_id
        if not self.token:
            self.token, self._expires = self._get_token()

    # Получение токена для работы с API
    def _get_token(self):
        params = {'yandexPassportOauthToken': self._oauth_token}
        response = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens', params=params)
        decode_response = response.content.decode('UTF-8')
        text = json.loads(decode_response)
        iam_token = text.get('iamToken')
        expires_iam_token = text.get('expiresAt')
        print(iam_token)
        return iam_token, expires_iam_token

    # Получение аудио по тексту используя Yandex SpeechKit
    def get_audio(self, text, lang='ru-RU', speaker='oksana', emotion='good', speed=1.0):
        # Формирование запроса
        url = 'https://tts.voicetech.yandex.net/generate'
        params = {
            'text': text,
            'format': 'opus',
            'lang': lang,
            'speaker': speaker,
            'emotion': emotion,
            'speed': speed,
            'key': self.token
        }
        # Получение ответа
        response = requests.get(url, params=params)
        # Проверка ответа
        if response.status_code == 200:
            return response.content
        else:
            raise Exception('Yandex SpeechKit API error: {}'.format(response.status_code))

    # Определить параметры запроса.
    def synthesize(self, text):
        url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
        headers = {
            'Authorization': 'Bearer ' + self.token,
        }

        data = {
            'text': text,
            'lang': 'ru-RU',
            'voice': 'filipp',
            'folderId': self.folder_id,
            'format': 'lpcm',
            'sampleRateHertz': 48000,
        }

        with requests.post(url, headers=headers, data=data, stream=True) as resp:
            if resp.status_code != 200:
                raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))

            for chunk in resp.iter_content(chunk_size=None):
                yield chunk


if __name__ == '__main__':
    api = SpeechKitApi("y0_AgAAAAA0njjuAATuwQAAAADfaQoqaNiIWvmKS1m6Oi5J6a2OhC4wCEU",
                       "b1gsekscneagltddk0rj")
    with open("hello.opus", "wb") as f:
        for audio_content in api.synthesize("Привет, мир!"):
            f.write(audio_content)
