import argparse
from pathlib import Path
from typing import Optional



def main(folder_path: str) -> None:
    
    try: 
        path = Path(folder_path)
    except TypeError:
        raise TypeError(f"Error: input {folder_path} is not a path")
        return
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: {folder_path} path is not found")
        return
    if not path.is_dir():
        raise TypeError(f"Error: {folder_path} is not a directory")
        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synchronize folder with API")
    parser.add_argument("path", type=str, help="Folder path to synchronise")
    
    args = parser.parse_args()
    main(args.path)