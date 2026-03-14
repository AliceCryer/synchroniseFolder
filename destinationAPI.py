import hashlib
import os
from pathlib import Path
from typing import Optional
import shutil

#to avoid circular import functions moved here, may need to refactor to seperate lib file
def get_file_hash(filepath: Path)-> str:
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def list_hashed_files(filepath: Path) -> dict:
    file_hashes = {}
    for root, _, files in os.walk(filepath):
        for file in files:
            full_path = os.path.join(root, file)
            relative = os.path.relpath(full_path, filepath)
            file_hashes[relative] = get_file_hash(full_path)
    return file_hashes

class destinationAPI: #change name to be more descriptive
    
    def __init__(self, base_dir: str | Path) -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
    
    def file_path(self, filename: str) -> Path:
        return Path(self.base_dir, filename)
    
    def create_file(self, filename: str, content: str = "") -> None:
        file_path = self.file_path(filename)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
    
    def update_file(self, filename: str, content: str) -> None:
        file_path = self.file_path(filename)
        if not file_path.exists():
            raise FileNotFoundError(f"File {filename} not found, cannot be updated")
        self.delete_file(filename)
        self.create_file(filename, content)

    
    def delete_file(self, filename: str) -> None:
        file_path = self.file_path(filename)
        if not file_path.exists():
            raise FileNotFoundError(f"File {filename} not found, cannot be deleted")
        os.remove(file_path)

    
    def get_file_hash(self,path)->str:
        return get_file_hash(self.file_path(path))

    def list_hashed_files(self, directory) ->dict:
        return list_hashed_files(self.file_path(directory))

