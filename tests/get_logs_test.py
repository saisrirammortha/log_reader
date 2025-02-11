import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, mock_open

from app.main import app  # Import the FastAPI app

client = TestClient(app)

LOG_DIRECTORY = "/var/log"

# Mocked log file content
mock_log_content = b"""INFO: Server started
ERROR: Disk failure
DEBUG: Connection established
WARN: High memory usage
INFO: User login successful
ERROR: Timeout error
"""


# Test: File name doesn't start with LOG_DIRECTORY (400 Bad Request)
def test_get_logs_invalid_filename():
    response = client.get("/api/v1/logs",
                          params={"file_name":"/invalid_path/logfile.log"})

    assert response.status_code == 400
    assert response.json()["message"] == "File name doesn't start with /var/log"


# Test: File doesn't exist (404 Not Found)
def test_get_logs_file_not_found(monkeypatch):
    with patch("os.path.exists", return_value=False):
        response = client.get("/api/v1/logs",
                              params={"file_name":"/var/log/missing.log"})

        assert response.status_code == 404
        assert response.json()["message"] == "File /var/log/missing.log doesn't exist"


# Test: Successfully fetch logs (200 OK)
def test_get_logs_success():
    with patch("os.path.exists", return_value=True), patch(
            "builtins.open", mock_open(read_data=mock_log_content)):
        response = client.get("/api/v1/logs",
                              params={"file_name":"/var/log/app.log", "entries":3})

        print(response.text)
        assert response.status_code == 200
        data = response.json()

        assert "logs" in data
        assert len(data["logs"]) == 3  # Should return last 3 lines
        assert "ERROR: Timeout error" in data["logs"]


# Test: Fetch logs with search filter
def test_get_logs_with_search():
    with patch("os.path.exists", return_value=True), patch(
            "builtins.open", mock_open(read_data=mock_log_content)):
        response = client.get("/api/v1/logs",
                              params={"file_name":"/var/log/app.log", "entries":5, "search":"ERROR"})
        print(response.text)
        assert response.status_code == 200
        data = response.json()

        assert len(data["logs"]) == 1  # Should return only "ERROR" lines
        assert "ERROR: Timeout error" in data["logs"]


# Test: Handle unexpected exceptions (500 Internal Server Error)
def test_get_logs_exception():
    with patch("os.path.exists", side_effect=Exception("Unexpected error")):
        response = client.get("/api/v1/logs", params={"file_name":"/var/log/app.log"})

        assert response.status_code == 500
        assert response.json()["message"] == "Unexpected error"