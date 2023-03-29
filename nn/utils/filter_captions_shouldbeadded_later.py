import torch
from sentence_transformers import SentenceTransformer, util
from transformers import AutoModelForSeq2SeqLM, T5TokenizerFast
import json


stop_words = ['Видео', 'ВИДЕО', 'видео']

def find_similarity(text1, text2):
    '''Функция, отвечающая за нахождение коэффициента схожести между двумя описаниями, где
    :param text1: первое описание;
    :param text2: второе описание'''
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    first_caption_embedding = model.encode(text1)
    second_caption_embedding = model.encode(text2)
    res = util.dot_score(first_caption_embedding, second_caption_embedding)
    #print("Similarity:", res)
    return res

def sum_text(text):
    '''Функция, отвечающая за обобщение текста описаний двух роликов, где
    :param text: описания для обобщения'''
    # Зададим название выбронной модели из хаба
    MODEL_NAME = 'UrukHan/t5-russian-summarization'
    MAX_INPUT = 256
    # Загрузка модели и токенизатора
    tokenizer = T5TokenizerFast.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    # Входные данные (можно массив фраз или текст)
    input_sequences = text
    task_prefix = "Spell correct: "  # Токенизирование данных
    if type(input_sequences) != list:
        input_sequences = [input_sequences]
    '''if torch.cuda.is_available():
        if use_gpu == 0:
            device = torch.device('cuda')
        else:
            device = torch.device('cuda:' + use_gpu)
    else:
        device = torch.device('cpu')'''
    device = torch.device('cpu')
    encoded = tokenizer(
        [task_prefix + sequence for sequence in input_sequences],
        padding="longest",
        max_length=MAX_INPUT,
        truncation=True,
        return_tensors="pt",
    )
    predicts = model.generate(**encoded.to(device))  # # Прогнозирование
    print(tokenizer.batch_decode(predicts, skip_special_tokens=True))
    return tokenizer.batch_decode(predicts, skip_special_tokens=True)[0]

def del_stop_words(text):
    '''Функция отвечающая за удаление стоп слов'''
    for word in stop_words:
        text = text.replace(word, "")
    return text

def filter_captions(path, dict):
    '''Функция, отвечающая за удаление похожих сцен из клипов, где
    :param dict: словарь с данными видео'''
    '''path_to_json = '/Users/macbook/Desktop/MTC TRUE TECH HACH/Проект/Перевод, озвучка и интеграция/Актуальные/captions-2.json'
    with open(path_to_json, 'r') as j:
        dict = json.loads(j.read())'''
    for film in dict:
        for key_clip, values_clip in dict[film].items():
            i = 0
            j = 1
            while j != len(list(dict[film][key_clip].keys())):
                if i == j:
                    j += 1
                else:
                    scene_1 = list(dict[film][key_clip])[i]
                    scene_2 = list(dict[film][key_clip])[j]
                    scene_1_end = dict[film][key_clip][scene_1]['end']
                    scene_2_start = dict[film][key_clip][scene_2]['start']
                    scene_caption_1 = dict[film][key_clip][scene_1]['caption']
                    scene_caption_2 = dict[film][key_clip][scene_2]['caption']
                    coef = find_similarity(scene_caption_1, scene_caption_2)
                    if coef >= 0.75 and (abs(scene_2_start - scene_1_end) / scene_1_end) * 100.0 <= 5.0:
                        texts = scene_caption_1 + '. ' + scene_caption_2
                        new_texts = sum_text([texts])
                        dict[film][key_clip][scene_1]['end'] = dict[film][key_clip][scene_2]['end']
                        dict[film][key_clip][scene_1]['caption'] = new_texts
                        dict[film][key_clip].pop(list(dict[film][key_clip])[j])
                    else:
                        j += 1
            i += 1
        return dict
        '''path_to_new = '/Users/macbook/Desktop/MTC TRUE TECH HACH/Проект/Перевод, озвучка и интеграция/Актуальные/new.json'
        with open(path_to_new, 'w', encoding="utf-8") as f:
            json.dump(dict, f, ensure_ascii=False)'''



#filter_captions()
#sum_text(['Мужчина идет по полю', 'Видео мужчина идет с рюкзаком на спине'])
