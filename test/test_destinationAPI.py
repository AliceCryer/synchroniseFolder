import hashlib

import pytest
import requests_mock
import requests
import os
from pathlib import Path
from destinationAPI import destinationAPI, get_file_hash, list_hashed_files

@pytest.fixture
def test_url():
    return "http://fake_url.fake/"

@pytest.fixture
def test_path()->Path:
    return Path(os.path.dirname(__file__))

@pytest.fixture
def test_dest(test_url: str) -> destinationAPI:
    return destinationAPI(test_url)

@pytest.fixture
def mock_response():
    with requests_mock.Mocker() as mock_request:
        yield mock_request

def test_create_file(test_dest: destinationAPI, test_url: str)->None:
    with requests_mock.Mocker() as mock_request:
        mock_request.post(f"{test_url}", status_code=200)
        test_dest.create_file("test.txt", "hello")
        assert mock_request.called
        assert mock_request.request_history[0].json() == {"path": "test.txt", "content": "hello"}

def test_delete_file(test_dest: destinationAPI, test_url:str, mock_response: requests_mock.Mocker)->None:
    mock_response.delete(f"{test_url}", status_code=404)
    with pytest.raises(requests.HTTPError):
        try:
            test_dest.update_file("missingfile.txt", "data")
        except requests_mock.exceptions.NoMockAddress:
            raise requests.HTTPError("No file found")

    mock_response.delete(test_dest.make_URL("del.txt"), status_code=200)
    test_dest.delete_file("del.txt")
    assert mock_response.called
    assert mock_response.request_history[-1].method == "DELETE"
    assert mock_response.request_history[-1].url == test_dest.make_URL("del.txt")


def test_get_file_hash(test_dest: destinationAPI, mock_response: requests_mock.Mocker)->None:
    mock_response.get(test_dest.make_URL("hashme.txt"), content=b"abc", status_code=200)
    expected = "900150983cd24fb0d6963f7d28e17f72"  # md5 of b"abc"
    assert test_dest.get_file_hash("hashme.txt") == expected

def test_list_hashed_files_success(test_url:str):
    class MockResponse:
        def __init__(self, url):
            self.url = url
            self.status_code = 200
            self._content = file_contents.get(url, b"")
        def json(self):
            return files
        def iter_content(self, chunk_size):
            yield self._content
        def raise_for_status(self):
            if self.status_code != 200:
                raise requests.HTTPError("fail")
        
    def mock_get(url, stream=False):
        if url == test_url:
            return MockResponse(url)
        return MockResponse(url)

    files = ["a.txt", "b.txt"]
    file_contents = {
        f"{test_url.rstrip('/')}/a.txt": b"foo",
        f"{test_url.rstrip('/')}/b.txt": b"bar"
    }
    file_hashes = {
        "a.txt": hashlib.md5(b"foo").hexdigest(),
        "b.txt": hashlib.md5(b"bar").hexdigest()
    }
    setattr(requests, "get", mock_get)
    with pytest.raises(requests.HTTPError):
        list_hashed_files(test_url)

    result = list_hashed_files(test_url)
    assert result == file_hashes
