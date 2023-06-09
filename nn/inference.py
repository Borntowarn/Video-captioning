import os

from utils.extract_clips import extract_clips
from utils.save_captions import save_captions
from utils.delete_files import delete_files

from utils.add_audio_to_video import add_audio_to_video
from utils.unite_audio import unite_audio
from utils.voice_text import voice_text
from utils.translate import translate

from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

def main(root_path, videos_path):
    model_id = 'damo/multi-modal_hitea_video-captioning_base_en'
    pipeline_caption = pipeline(Tasks.video_captioning, model=model_id, device='cuda')
    all_result_lists = extract_clips(root_path, 50)
    print(all_result_lists)
    for path, folders, files in os.walk(os.path.join(root_path, videos_path)):
        for scene in files:
            print("NORM PATH", os.path.normpath(path))
            try:
                video, clip = str(os.path.normpath(path)).split("\\")[-2:]
            except Exception as _:
                # Ubuntu likes / not \
                video, clip = str(os.path.normpath(path)).split("/")[-2:]
            scene_path = os.path.join(path, scene)
            print(scene_path)

            start = all_result_lists[video][clip + '.mp4'][scene]['start']
            end = all_result_lists[video][clip + '.mp4'][scene]['end']
            min_length = int((end - start) * 1.3)

            pipeline_caption.model.model.beam_generator.min_length = min_length
            # pipeline_caption.model.model.beam_generator.max_length = max_length
            pipeline_caption.model.model.beam_generator.beam_size = 5
            output = pipeline_caption(scene_path)
            output['caption'] = translate(output['caption'])
            all_result_lists[video][clip + '.mp4'][scene].update(output)

    save_captions(root_path, all_result_lists)
    voice_text(root_path, all_result_lists)
    unite_audio(root_path, all_result_lists)
    add_audio_to_video(root_path)


if __name__ == '__main__':
    root_path = 'inference_videos'
    videos_path = 'clips'
    # Проверка наличия папки inference_videos
    if not os.path.exists(root_path):
        os.makedirs(root_path)
    # Проверка наличия папки clips внутри inference_videos
    if not os.path.exists(os.path.join(root_path, videos_path)):
        os.makedirs(os.path.join(root_path, videos_path))
    main(root_path, videos_path)
    delete_files(root_path)
