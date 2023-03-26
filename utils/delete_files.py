import os
import shutil

def delete_files(root_path):
    for r_path in os.listdir(root_path):
        if r_path != 'videos':
            r_path = os.path.join(root_path, r_path)
            if os.path.isdir(r_path):
                for path in os.listdir(r_path):
                    path = os.path.join(r_path, path)
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                    else:
                        os.remove(path)
            else:
                os.remove(r_path)