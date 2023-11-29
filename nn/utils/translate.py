# folder_id = 'b1giso3qle0a0jtnj2bh'
# target_language = 'ru'

# body = {
#     "targetLanguageCode": target_language,
#     "texts": [],
#     "folderId": folder_id,
# }

# headers = {
#     "Content-Type": "application/json",
#     "Authorization": "Bearer {0}".format(IAM_TOKEN)
# }

# response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
#                     json = body,
#                     headers = headers
#                 )
#                 translation = json.loads(response.text)['translations'][0]['text']

from googletrans import Translator

def translate(input_text):
    translator = Translator()
    return translator.translate(input_text, src='en', dest='ru').text
