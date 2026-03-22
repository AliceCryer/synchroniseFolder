import hashlib
from typing import Optional
import requests
import urllib.request as urllib2
from urllib.parse import unquote


# may need to refactor to seperate lib file with the path based version
def get_file_hash(url: str) -> str:
    with requests.get(url, stream=True) as resp:
        resp.raise_for_status()
        hasher = hashlib.md5()
        for chunk in resp.iter_content(4096):
            hasher.update(chunk)
        return hasher.hexdigest()

def list_hashed_files(file_url: str) -> dict:
    file_hashes = {}
    resp = requests.get(file_url)
    resp.raise_for_status()
    try:
        files = resp.json()
    except requests.JSONDecodeError:
        return file_hashes
    for file in files:
        full_path = f"{file_url.rstrip('/')}/{file}"
        file_hashes[file] = get_file_hash(full_path)
    return file_hashes

class destinationAPI(): #change name to be more descriptive
    def __init__(self, base_url: str ) -> None:
        self.base_url = base_url.rstrip('/')
    
    def make_URL(self, filename: str) -> str:
        decoded_filename = unquote(filename)
        normalized_filename = decoded_filename.replace("\\", "/")
        return f"{self.base_url}/{normalized_filename}"
    
    def create_file(self, filename: str, content: str = "") -> None:
        if not filename:
            return
        requests.put(self.make_URL(filename), json={"path": filename, "content": content}).raise_for_status()
    
    def update_file(self, filename: str, content: str) -> None:
        if not filename:
            return
        self.delete_file(filename)
        self.create_file(filename, content)

    def delete_file(self, filename: str) -> None:
        if not filename:
            return
        requests.delete(self.make_URL(filename)).raise_for_status()

    def get_file_hash(self, filename: str) -> str:
        return get_file_hash(self.make_URL(filename))

    def list_hashed_files(self) ->dict:
        return list_hashed_files(self.base_url)

