import os
import json

def save_captions(root_path, result):
    caption_path = os.path.join(root_path, "captions.json")
    with open(caption_path, "w", encoding='utf-8') as writer:
        json.dump(result, writer, ensure_ascii=False, indent='  ')