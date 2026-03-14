import pytest
from pathlib import Path
import json
import builtins
import main
import json

@pytest.fixture
def test_config_file(test_path: Path)-> dict:
    config = {"destinationUrl": str(test_path +"/" + "dest")}
    return config

def test_json_loader(test_path: Path)-> None:
    data = {"key": "value"}
    with open(Path.joinpath(test_path, "test.json"), 'w') as f:
        json.dump(data, f)
    assert main.json_loader('test.json') == data

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
    dest = {"a.txt": "hash1", "c.txt": "hash3"}
    to_copy, to_delete = main.compare_directories(src, dest)
    assert "b.txt" in to_copy
    assert "c.txt" in to_delete
    assert "a.txt" not in to_copy
    assert "a.txt" not in to_delete

def test_main_source_not_dir(test_path: Path)-> None:
    file = Path.joinpath(test_path, "file.txt")
    file.write_text("data")
    with pytest.raises(TypeError):
        main.main(str(file))

def test_main_config_missing(test_path: Path)-> None:
    src_dir = Path.joinpath(test_path, "src")
    src_dir.mkdir()
    setattr(main, "makePath", lambda path_under_test: Path(path_under_test))
    with pytest.raises(FileNotFoundError):
        main.main(str(src_dir))

def test_main_config_invalid(test_path: Path)-> None:
    src_dir = Path.joinpath(test_path, "src")
    src_dir.mkdir()
    setattr(main, "makePath", lambda path_under_test: Path(path_under_test))
    setattr(main, "json_loader", lambda p: None)
    with pytest.raises(ValueError):
        main.main(str(src_dir))

def test_main_no_destination_url(test_path: Path)-> None:
    src_dir = Path.joinpath(test_path, "src")
    src_dir.mkdir()
    setattr(main, "makePath", lambda path_under_test: Path(path_under_test))
    setattr(main, "json_loader", lambda p: {})
    with pytest.raises(ValueError):
        main.main(str(src_dir))

def test_main_success(test_path: Path, test_config_file: dict)-> None:
    src_dir = Path.joinpath(test_path, "src")
    dest_dir = Path.joinpath(test_path, "dest")
    src_dir.mkdir()
    dest_dir.mkdir()
    config_path = test_config_file
    (src_dir / "file.txt").write_text("data")

    # Patch makePath to handle config and destination
    setattr(main, "makePath", lambda path_under_test: Path(path_under_test))
    setattr(main, "json_loader", lambda path_under_test: {"destinationUrl": str(dest_dir)})
    setattr(main, "sync_folder", lambda s, d: None)

    main.main(str(src_dir))