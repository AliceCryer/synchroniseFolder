import argparse
import hashlib
import os
from pathlib import Path
from typing import Optional
import json
from urllib.parse import urlparse

import destinationAPI

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

def json_loader(filepath: Path) -> dict:
    with open(filepath, 'r') as file_descriptor:
        data = json.load(file_descriptor)
    return data

def sync_folder(source_filepath: Path, destination_url: str) -> None:
    destAPI = destinationAPI.destinationAPI(destination_url)
    src_hashes = list_hashed_files(source_filepath)
    dest_hashes = destAPI.list_hashed_files()
    to_be_created, to_be_updated, to_be_deleted = compare_directories(src_hashes, dest_hashes)
    for file in to_be_created:
        content = Path(os.path.join(source_filepath, file)).read_text()
        destAPI.create_file(file, content)
    for file in to_be_updated:
        content = Path(os.path.join(source_filepath, file)).read_text()
        destAPI.update_file(file, content)
    for file in to_be_deleted:
        destAPI.delete_file(file)
    

def compare_directories(src_hashes: dict, dest_hashes: dict)-> tuple[list[str], list[str]]:
    to_be_created = []
    to_be_updated = []
    to_be_deleted = []

    for file, hash_val in src_hashes.items():
        if file not in dest_hashes:
            to_be_created.append(file)
        
        elif dest_hashes[file] != hash_val:
            to_be_updated.append(file)
        else:
            pass

    for file in dest_hashes:
        if file not in src_hashes:
            to_be_deleted.append(file)

    return to_be_created, to_be_updated, to_be_deleted

def makeURL(url: str) -> str:
    return urlparse(url)

def makePath(path: str | Path) -> Optional[Path]:
    try: 
        path = Path(os.path.abspath(path)) #uses cwd, need refactor
    except TypeError:
        raise TypeError(f"Error: input {path} is not a path")
        return
    if not path.exists():
        raise FileNotFoundError(f"Error: {path} path is not found")
        return

    else:
        return path

def main(source_path: str | Path) -> None:
    source_filepath = makePath(source_path)
    if not source_filepath.is_dir():
        raise TypeError(f"Error: {source_filepath} is not a directory")
        return
    else:
            #load destination url from config file, security implications?
            #check compatibility rel and abs url and unix vs windows
        config = json_loader(makePath("config.json")) #refactor to make a command line argument
        if not config:
            raise ValueError("Error: Invalid config.json")
            return
        destination_url = config.get("destinationUrl")
        if not destination_url:
            raise ValueError("Error: destinationUrl not found in config.json")
            return
        destination_url = makeURL(destination_url)
        if not destination_url.scheme or not destination_url.netloc:
            raise ValueError(f"Error: Invalid destinationUrl {destination_url}")
            return
        sync_folder(source_filepath, destination_url) #refactor to run at recurring intervals or on detected change


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synchronize folder with API")
    parser.add_argument("source_path", type=str, help="Path of source folder to be synchronised")
    
    args = parser.parse_args()
    main(args.source_path)