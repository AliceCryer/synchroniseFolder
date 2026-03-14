import pytest
import os
from pathlib import Path
from destinationAPI import destinationAPI, get_file_hash, list_hashed_files

@pytest.fixture
def test_path():
    return Path(os.path.dirname(__file__))

@pytest.fixture
def test_dest(test_path):
    return destinationAPI(test_path)

def test_create_file(test_dest):
    test_dest.create_file("test.txt", "hello")
    assert (Path.joinpath(test_dest.base_dir, "test.txt")).exists()
    os.remove(Path.joinpath(test_dest.base_dir, "test.txt"))
    
    test_dest.create_file("a/b/c.txt", "data")
    assert (Path.joinpath(test_dest.base_dir, "a/b/c.txt")).exists()
    os.remove(Path.joinpath(test_dest.base_dir, "a/b/c.txt"))
    os.rmdir(Path.joinpath(test_dest.base_dir, "a/b"))
    os.rmdir(Path.joinpath(test_dest.base_dir, "a"))
    
def test_update_file_raises_if_not_exists(test_dest):
    with pytest.raises(FileNotFoundError):
        test_dest.update_file("nofile.txt", "data")

def test_delete_file(test_dest):
    with pytest.raises(FileNotFoundError):
        test_dest.delete_file("missing.txt")

    test_dest.create_file("del.txt", "bye")
    test_dest.delete_file("del.txt")
    assert not (Path.joinpath(test_dest.base_dir, "del.txt")).exists()

def test_get_file_hash(test_dest):
    test_dest.create_file("hashme.txt", "abc")
    hash1 = test_dest.get_file_hash("hashme.txt")
    hash2 = get_file_hash(Path.joinpath(test_dest.base_dir, "hashme.txt"))
    assert hash1 == hash2
    os.remove(Path.joinpath(test_dest.base_dir, "hashme.txt"))

def test_hashed_files(test_dest):
    test_dest.create_file("file1.txt", "a")
    test_dest.create_file("file2.txt", "b")
    hashes = test_dest.list_hashed_files(".")
    assert "file1.txt" in hashes and "file2.txt" in hashes
    assert hashes["file1.txt"] == get_file_hash(Path.joinpath(test_dest.base_dir, "file1.txt"))
    assert hashes["file2.txt"] == get_file_hash(Path.joinpath(test_dest.base_dir, "file2.txt"))
    os.remove(Path.joinpath(test_dest.base_dir, "file1.txt"))
    os.remove(Path.joinpath(test_dest.base_dir, "file2.txt"))
