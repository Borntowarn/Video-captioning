import os
from pydub import AudioSegment
import json



def unite_audio(path, dict):
    path_generated_audio = os.path.join(path, 'generated_audio')
    for key_film in dict:
        audio_origin = os.path.join(path, 'audios', f'{key_film}.wav')
        overlay_audio = AudioSegment.from_wav(audio_origin)
        for key_clip, values_clip in dict[key_film].items():
            key_clip_num, ext = key_clip.split('.')
            buf = -999.0
            for key_scene, value_scene in dict[key_film][key_clip].items():
                key_scene_num, ext = key_scene.split('.')
                path_to_gen_audio = f"{path_generated_audio}/{key_film}/{key_clip_num}/{key_scene_num}.wav"
                if value_scene['start'] == buf or (abs(value_scene['start'] - buf) / buf) * 100.0 <= 10.0:
                    audio_2 = AudioSegment.from_file_using_temporary_files(path_to_gen_audio)
                    overlay_audio = overlay_audio.overlay(audio_2, position=(value_scene['start'] + 0.5) * 1000)
                else:
                    audio_2 = AudioSegment.from_file_using_temporary_files(path_to_gen_audio)
                    overlay_audio = overlay_audio.overlay(audio_2, position=value_scene['start'] * 1000)
                buf = value_scene['end']
        overlay_audio.export(f'{path}/audios/{key_film}.wav', format='wav')