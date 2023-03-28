import json
import os
import torch
import torchaudio


def voice_text(path, dict):
    '''Функция, отвечающая за перевод сгенерированного текста и его озвучивание
    :param path: путь к папке inference_video'''
    films = os.listdir(os.path.join(path, 'videos'))
    generated_audio_folder = os.path.join(path, 'generated_audio')
    if not os.path.isdir(generated_audio_folder):
        os.mkdir(generated_audio_folder)
    language = 'ru'
    model_id = 'v3_1_ru'
    sample_rate = 48000
    speaker = 'xenia'
    model, exapmle_text = torch.hub.load(repo_or_dir='snakers4/silero-models', model='silero_tts',
                                         language=language, speaker=model_id)
    # model.to(device)  # gpu or cpu
    for film in films:
        for key_clip, values_clip in dict[film].items():
            for key_scene, value_scene in dict[film][key_clip].items():
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
                audio = model.apply_tts(text=value_scene['caption'] + '.',
                                        speaker=speaker,
                                        sample_rate=sample_rate)
                torchaudio.save(gen_audio_path, audio.unsqueeze(0), sample_rate)