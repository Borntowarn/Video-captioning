from googletrans import Translator
#from google.cloud import texttospeech
import os
import pyttsx3
import torch
import importlib
import json


def translate_and_voice(path, dict):
    '''Функция, отвечающая за перевод сгенерированного текста и его озвучивание
    :param path: путь к папке inference_video'''
    translator = Translator()
    films = os.listdir(os.path.join(path, 'videos'))
    generated_audio_folder = os.path.join(path, 'generated_audio')
    if not os.path.isdir(generated_audio_folder):
        os.mkdir(generated_audio_folder)
    for film in films:
        for key_clip, values_clip in dict[film].items():
            for key_scene, value_scene in dict[film][key_clip].items():
                importlib.reload(pyttsx3)
                engine = pyttsx3.init(driverName='sapi5')
                voices = engine.getProperty("voices")
                engine.setProperty("rate", 200)
                # voices[45].id - Юрий, voices[27].id - Милена
                engine.setProperty("voice", voices[0].id)
                translation = translator.translate(value_scene['caption'], src='en', dest='ru')
                film_num, ext = os.path.splitext(film)
                clip_num, ext = os.path.splitext(key_clip)
                scene_num, ext = os.path.splitext(key_scene)
                gen_audio_film_path = f'{generated_audio_folder}/{film_num}'
                if not os.path.isdir(gen_audio_film_path):
                    os.mkdir(gen_audio_film_path)
                gen_audio_clip_path = f'{gen_audio_film_path}/{clip_num}'
                if not os.path.isdir(gen_audio_clip_path):
                    os.mkdir(gen_audio_clip_path)
                gen_audio_path = f'{gen_audio_clip_path}/{scene_num}.wav'
                engine.save_to_file(translation.text, gen_audio_path)
                engine.runAndWait()
                #print('Выполнено {}'.format(key_scene))