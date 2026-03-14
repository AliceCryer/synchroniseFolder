import hashlib
import os
from pathlib import Path
import pathlib
from typing import Optional
import shutil
from main import get_file_hash, list_files_with_hashes

class FileSyncAPI:
    
    def __init__(self, base_dir: str | Path) -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
    
    def file_path(self, filename: str) -> Path:
        return pathlib.PurePath(self.base_dir, filename)
    
    def create_file(self, filename: str, content: str = "") -> None:
        file_path = self.file_path(filename)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        print(f"File {filename} created successfully")
    
    def update_file(self, filename: str, content: str) -> None:
        file_path = self.file_path(filename)
        if not file_path.exists():
            raise FileNotFoundError(f"File {filename} not found")
        print(f"File {filename} updated successfully")

    
    def delete_file(self, filename: str) -> None:
        file_path = self.file_path(filename)
        if not file_path.exists():
            raise FileNotFoundError(f"File {filename} not found")
        os.remove(file_path)
        print(f"File {filename} deleted successfully")

    
    def get_file_hash(self,path)->str:
        return get_file_hash(self.file_path(path))

    def list_files_with_hashes(self, directory) ->dict:
        return list_files_with_hashes(self.file_path(directory))

