from moviepy.editor import VideoFileClip, AudioFileClip
import os


def add_audio_to_video(path):
    '''Функция наложения созданного тифлокомментария на видео, где
        :param path - путь к папке inference_video'''
    film_with_audiodescr = 'films_with_audiodescr'
    #Создание папки для фильмов с аудиодескрипцией
    if not os.path.isdir(film_with_audiodescr):
        os.mkdir(film_with_audiodescr)
    films = os.listdir(os.path.join(path, 'videos'))
    films.sort()
    audios = os.listdir(os.path.join(path, 'audios'))
    audios.sort()
    films_audios = list(zip(films, audios))
    for item in films_audios:
        video_name, ext = item[0].split('.')
        video_clip = VideoFileClip(f'{path}/videos/{item[0]}')
        audio_clip = AudioFileClip(f'{path}/audios/{item[1]}')
        #Замена оригинальной аудиодорожки на новую с аудиодескрипцией
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile(f"{film_with_audiodescr}/{video_name}.mp4", audio_codec='aac')
        
        video_clip.close()
        audio_clip.close()
        final_clip.close()

add_audio_to_video('inference_videos')
