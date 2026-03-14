import argparse
import os
from pathlib import Path
from time import time
import sched
from typing import Optional
import json
import destinationAPI

def json_loader(filepath: Path) -> dict:
    with open(filepath, 'r') as file_descriptor:
        data = json.load(file_descriptor)
    return data

def sync_folder(source_filepath: Path, dest_filepath: Path) -> None:
    src_hashes = destinationAPI.list_hashed_files(source_filepath)
    dest_hashes = destinationAPI.list_hashed_files(dest_filepath)
    to_be_copied, to_be_deleted = compare_directories(src_hashes, dest_hashes)
    

def compare_directories(src_hashes: dict, dest_hashes: dict)-> tuple[list[str], list[str]]:
    to_be_copied = []
    to_be_deleted = []

    for file, hash_val in src_hashes.items():
        if file not in dest_hashes or dest_hashes[file] != hash_val:
            to_be_copied.append(file)

    for file in dest_hashes:
        if file not in src_hashes:
            to_be_deleted.append(file)

    return to_be_copied, to_be_deleted

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
        try:
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
            destination_filepath = makePath(destination_url)

        except FileNotFoundError:
            raise FileNotFoundError("Error: config.json not found")
            return
        sync_folder(source_filepath, destination_filepath) #refactor to run at recurring intervals or on detected change


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synchronize folder with API")
    parser.add_argument("source_path", type=str, help="Path of source folder to be synchronised")
    
    args = parser.parse_args()
    main(args.source_path)