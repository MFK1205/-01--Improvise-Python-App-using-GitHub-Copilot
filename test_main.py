"""Tests for the FastAPI text-generation application."""

import hashlib

from fastapi.testclient import TestClient

from main import TextData, app, generate

client = TestClient(app)


def test_read_root_returns_leenasree_welcome_message():
    """Test the customized welcome message."""
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the API, Leenasree!"
    }


def test_generate_returns_whitespace_separated_tokens():
    """Test token generation from input text."""
    response = client.post(
        "/generate/",
        json={"text": "FastAPI makes testing straightforward"},
    )

    assert response.status_code == 200
    assert response.json()["tokens"] == [
        "FastAPI",
        "makes",
        "testing",
        "straightforward",
    ]


def test_generate_returns_md5_checksum_of_input_text():
    """Test MD5 checksum generation."""
    text = "checksum this text"

    response = client.post("/generate/", json={"text": text})

    assert response.status_code == 200
    assert response.json()["checksum"] == hashlib.md5(
        text.encode("utf-8")
    ).hexdigest()


def test_generate_empty_text_returns_empty_token_list():
    """Test empty text input."""
    response = client.post("/generate/", json={"text": ""})

    assert response.status_code == 200
    assert response.json()["tokens"] == []


def test_generate_missing_text_returns_unprocessable_entity():
    """Test missing required text field."""
    response = client.post("/generate/", json={})

    assert response.status_code == 422


def test_generate_non_string_text_returns_unprocessable_entity():
    """Test invalid text data type."""
    response = client.post(
        "/generate/",
        json={"text": ["not", "a", "string"]},
    )

    assert response.status_code == 422


def test_generate_function_accepts_text_data_model():
    """Test direct invocation of the generate function."""
    data = TextData(text="direct function call")

    result = generate(data)

    assert result["tokens"] == ["direct", "function", "call"]
