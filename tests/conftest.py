from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_session():
    """Create a mock requests session."""
    from unittest.mock import MagicMock

    session = MagicMock()
    return session


@pytest.fixture
def mock_response():
    """Create a mock response."""
    response = MagicMock()
    response.status_code = 200
    response.text = "test"
    response.headers = {
        "Server": "nginx",
        "Date": "Mon, 01 Jan 2024 00:00:00 GMT",
        "Content-Type": "text/html",
    }
    return response


@pytest.fixture
def sample_urls():
    """Sample URLs for testing."""
    return [
        "http://example.com",
        "http://example.com/page?id=1",
        "https://example.com/admin/login",
    ]


@pytest.fixture
def sample_html_forms():
    """Sample HTML with forms for testing."""
    return """
    <form action="/login" method="post">
        <input type="text" name="username">
        <input type="password" name="password">
        <input type="submit" value="Login">
    </form>
    """


@pytest.fixture
def sample_html_index_of():
    """Sample HTML with directory listing."""
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Index of /</title></head>
    <body>
    <h1>Index of /</h1>
    <a href="/file.txt">file.txt</a>
    </body>
    </html>
    """
