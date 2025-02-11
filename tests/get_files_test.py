import sys; print('Python %s on %s' % (sys.version, sys.platform))
sys.path.extend(['/Users/bytedance/PycharmProjects/log_reader'])
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app  # Import the FastAPI app

client = TestClient(app)  # Initialize test client

# Mocked file structure
mocked_files = [
    ("/logs", [], ["file1.log", "file2.log"]),
    ("/logs/subdir", [], ["file3.log"]),
]


# Test: Fetch all files without search
def test_get_files_no_search():
    with patch("os.walk", return_value=mocked_files):
        response = client.get("/api/v1/files")  # Call the API

        assert response.status_code == 200
        data = response.json()

        assert "files" in data
        assert len(data["files"]) == 3
        assert any("file1.log" in f for f in data["files"])
        assert any("file2.log" in f for f in data["files"])
        assert any("file3.log" in f for f in data["files"])


# Test: Fetch files with a search
def test_get_files_with_search():
    with patch("os.walk", return_value=mocked_files):
        response = client.get("/api/v1/files?search=subdir")  # Call API with search

        assert response.status_code == 200
        data = response.json()

        assert len(data["files"]) == 1
        assert "file3.log" in data["files"][0]


# Test: Handle exception
def test_get_files_exception():
    with patch("os.walk", side_effect=Exception("Unexpected error")):
        response = client.get("/api/v1/files")  # Simulate failure

        assert response.status_code == 500
        assert response.json()["message"] == "Unexpected error"
