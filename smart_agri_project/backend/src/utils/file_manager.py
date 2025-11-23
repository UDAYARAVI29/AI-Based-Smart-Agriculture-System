import os
import shutil
import pandas as pd

def ensure_dir(path: str):
    """Create folder if missing."""
    os.makedirs(path, exist_ok=True)

def save_temp_file(uploaded_file, save_dir="temp_uploads"):
    ensure_dir(save_dir)
    file_path = os.path.join(save_dir, uploaded_file.filename)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.file.read())

    return file_path

def remove_file(path: str):
    if os.path.exists(path):
        os.remove(path)

def load_csv(path: str):
    return pd.read_csv(path)

def copy_folder(src, dst):
    ensure_dir(dst)
    shutil.copytree(src, dst, dirs_exist_ok=True)
