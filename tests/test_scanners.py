from unittest.mock import MagicMock, patch

from paranoic_scan.scanners import (
    encode_md5,
    find_paths,
    http_fingerprint,
    port_scan,
    scan_bypass,
    scan_lfi,
    scan_panel,
    scan_sqli,
    scan_xss,
)


class TestEncodeMD5:
    """Tests for encode_md5 function."""

    def test_encode_basic(self):
        """Test basic MD5 encoding."""
        assert encode_md5("test") == "098f6bcd4621d373cade4e832627b4f6"

    def test_encode_empty(self):
        """Test empty string."""
        assert encode_md5("") == "d41d8cd98f00b204e9800998ecf8427e"

    def test_encode_password(self):
        """Test password encoding."""
        assert encode_md5("password") == "5f4dcc3b5aa765d61d8327deb882cf99"


class TestScanPanel:
    """Tests for scan_panel function."""

    @patch("paranoic_scan.scanners.requests.Session")
    def test_scan_panel_found(self, mock_session_class):
        """Test panel found."""
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        mock_session.get.return_value = MagicMock(status_code=200)

        result = scan_panel("http://example.com", count=1)
        assert isinstance(result, list)

    @patch("paranoic_scan.scanners.requests.Session")
    def test_scan_panel_not_found(self, mock_session_class):
        """Test panel not found."""
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        mock_session.get.return_value = MagicMock(status_code=404)

        result = scan_panel("http://example.com", count=1)
        assert result == []


class TestScanSQLi:
    """Tests for scan_sqli function."""

    @patch("paranoic_scan.scanners.requests.Session")
    def test_sqli_vulnerable(self, mock_session_class):
        """Test SQLi detected."""
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        mock_response = MagicMock()
        mock_response.text.lower.return_value = "you have an error in your sql syntax"
        mock_session.get.return_value = mock_response

        result = scan_sqli("http://example.com?id=1")
        assert result is True

    @patch("paranoic_scan.scanners.requests.Session")
    def test_sqli_not_vulnerable(self, mock_session_class):
        """Test SQLi not detected."""
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        mock_response = MagicMock()
        mock_response.text.lower.return_value = "no error"
        mock_session.get.return_value = mock_response

        result = scan_sqli("http://example.com?id=1")
        assert result is False


class TestScanLFI:
    """Tests for scan_lfi function."""

    @patch("paranoic_scan.scanners.requests.Session")
    def test_scan_lfi_found(self, mock_session_class):
        """Test LFI file found."""
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        mock_response = MagicMock()
        mock_response.text.lower.return_value = "no such file or directory"
        mock_session.get.return_value = mock_response

        result = scan_lfi("http://example.com?file=")
        assert isinstance(result, list)

    @patch("paranoic_scan.scanners.requests.Session")
    def test_scan_lfi_default_files(self, mock_session_class):
        """Test LFI with default files."""
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        mock_response = MagicMock()
        mock_response.text.lower.return_value = "no error"
        mock_session.get.return_value = mock_response

        result = scan_lfi("http://example.com?file=")
        assert isinstance(result, list)


class TestScanXSS:
    """Tests for scan_xss function."""

    @patch("paranoic_scan.scanners.requests.Session")
    def test_scan_xss(self, mock_session_class):
        """Test XSS scanning."""
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        mock_response = MagicMock()
        mock_response.text = "<form><input name='q'></form>"
        mock_session.get.return_value = mock_response

        result = scan_xss("http://example.com")
        assert isinstance(result, list)


class TestScanBypass:
    """Tests for scan_bypass function."""

    @patch("paranoic_scan.scanners.requests.Session")
    def test_bypass_not_found(self, mock_session_class):
        """Test bypass not found."""
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        mock_response = MagicMock()
        mock_response.text = "incorrect login"
        mock_session.get.return_value = mock_response
        mock_session.post.return_value = mock_response

        result = scan_bypass("http://example.com/login")
        assert result is None


class TestFindPaths:
    """Tests for find_paths function."""

    @patch("paranoic_scan.scanners.requests.Session")
    def test_find_paths(self, mock_session_class):
        """Test path finding."""
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        mock_response = MagicMock()
        mock_response.text = "Index of /"
        mock_session.get.return_value = mock_response

        result = find_paths("http://example.com")
        assert isinstance(result, list)


class TestHTTPFingerprint:
    """Tests for http_fingerprint function."""

    @patch("paranoic_scan.scanners.requests.Session")
    def test_fingerprint(self, mock_session_class):
        """Test HTTP fingerprinting."""
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        mock_response = MagicMock()
        mock_response.headers = {
            "Server": "nginx",
            "Date": "NOW",
            "Content-Type": "text/html",
            "Connection": "keep-alive",
        }
        mock_session.get.return_value = mock_response

        result = http_fingerprint("http://example.com")
        assert isinstance(result, dict)
        assert result.get("server") == "nginx"
        assert result.get("date") == "NOW"

    @patch("paranoic_scan.scanners.requests.Session")
    def test_fingerprint_empty_headers(self, mock_session_class):
        """Test HTTP fingerprint with empty headers."""
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        mock_response = MagicMock()
        mock_response.headers = {}
        mock_session.get.return_value = mock_response

        result = http_fingerprint("http://example.com")
        assert result.get("server") == "Unknown"
        assert result.get("date") == ""


class TestPortScan:
    """Tests for port_scan function."""

    @patch("paranoic_scan.scanners.socket.socket")
    def test_port_scan_open(self, mock_socket_class):
        """Test open port detected."""
        mock_socket = MagicMock()
        mock_socket_class.return_value = mock_socket
        mock_socket.connect_ex.return_value = 0

        result = port_scan("127.0.0.1", [80])
        assert isinstance(result, dict)

    @patch("paranoic_scan.scanners.socket.socket")
    def test_port_scan_closed(self, mock_socket_class):
        """Test closed port not detected."""
        mock_socket = MagicMock()
        mock_socket_class.return_value = mock_socket
        mock_socket.connect_ex.return_value = 1

        result = port_scan("127.0.0.1", [80])
        assert result == {}


class TestScannerEdgeCases:
    """Edge case tests."""

    @patch("paranoic_scan.scanners.requests.Session")
    def test_network_timeout(self, mock_session_class):
        """Test network timeout handling."""
        import requests

        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        mock_session.get.side_effect = requests.RequestException("Timeout")

        result = scan_panel("http://example.com")
        assert result == []

    @patch("paranoic_scan.scanners.requests.Session")
    def test_sqli_network_error(self, mock_session_class):
        """Test network error handling for SQLi."""
        import requests

        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        mock_session.get.side_effect = requests.RequestException("Network error")

        result = scan_sqli("http://example.com?id=1")
        assert result is False
