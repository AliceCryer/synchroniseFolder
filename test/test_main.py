import os

import pytest
from pathlib import Path
import json
import builtins
import main

@pytest.fixture
def test_path()->Path:
    return Path(os.path.dirname(__file__))

@pytest.fixture
def src_dir(test_path: Path):
    src = Path.joinpath(test_path, "src")
    src.mkdir(exist_ok=True)
    yield src
    os.rmdir(src)

@pytest.fixture
def dest_url()->str:
    return "http://fake_url.fake/"

@pytest.fixture
def test_config_file(dest_url: str)-> dict:
    config = {"destinationUrl": dest_url}
    return config

def test_json_loader(test_path: Path)-> None:
    data = {"key": "value"}
    with open(Path.joinpath(test_path, "test.json"), 'w') as f:
        json.dump(data, f)
    assert main.json_loader(Path.joinpath(test_path, "test.json")) == data
    os.remove(Path.joinpath(test_path, "test.json"))

def test_makePath(test_path: Path)-> None:
    with pytest.raises(FileNotFoundError):
        main.makePath("not_path")
    with pytest.raises(TypeError):
        main.makePath(123)

    path_under_test = main.makePath(test_path)
    assert isinstance(path_under_test, Path)
    assert path_under_test.exists()

def test_compare_directories()-> None:
    src = {"a.txt": "hash1", "b.txt": "hash2"}
    dest = {"a.txt": "hash1", "b.txt": "hash3", "c.txt": "hash4"}
    to_add, to_update, to_delete = main.compare_directories(src, dest)
    assert "b.txt" in to_update
    assert "c.txt" in to_delete

    assert "a.txt" not in to_add
    assert "a.txt" not in to_update
    assert "a.txt" not in to_delete

def test_main_source_not_dir(test_path: Path)-> None:
    file = Path.joinpath(test_path, "file.txt")
    file.write_text("data")
    with pytest.raises(TypeError):
        main.main(str(file))

def test_main_config_invalid(src_dir: Path)-> None:
    setattr(main, "makePath", lambda path_under_test: Path(path_under_test))
    setattr(main, "json_loader", lambda p: None)
    with pytest.raises(ValueError):
        main.main(str(src_dir))

def test_main_no_destination_url(src_dir: Path)-> None:
    setattr(main, "makePath", lambda path_under_test: Path(path_under_test))
    setattr(main, "json_loader", lambda p: {})
    with pytest.raises(ValueError):
        main.main(str(src_dir))

def test_main_success(src_dir: Path, dest_url: str, test_config_file: dict)-> None:
    config_path = test_config_file
    Path(os.path.join(src_dir , "file.txt")).write_text("data")

    setattr(main, "makePath", lambda path_under_test: Path(path_under_test))
    setattr(main, "json_loader", lambda json: {"destinationUrl": dest_url})
    setattr(main, "sync_folder", lambda s, d: None)

    main.main(str(src_dir))
    os.remove(os.path.join(src_dir, "file.txt"))