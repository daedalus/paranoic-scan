# SPEC.md — paranoic-scan

## Purpose
Python security assessment tool for self-auditing web applications. Scans for common vulnerabilities including SQL injection, XSS, LFI, RFI, admin panel discovery, and more. This is a CLI tool that provides various security scanning capabilities for authorized security testing.

## Scope
- What IS in scope:
  - Web vulnerability scanning (SQLi, XSS, LFI, RFI, FSD)
  - Admin panel/path discovery
  - HTTP fingerprinting and port scanning
  - Hash encoding (MD5)
  - Encoder/decoder utilities (Base64, Hex, URL, Binary, ASCII)
- What is NOT in scope:
  - Exploit execution (scanning/detection only)
  - MySQL client (not implemented)
  - Exploit-DB integration (not implemented)

## Public API / Interface

### CLI Commands
| Command | Description |
|---------|-------------|
| `panel` | Find admin login pages |
| `sqli` | Scan for SQL injection |
| `lfi` | Scan for LFI vulnerabilities |
| `xss` | Scan for XSS vulnerabilities |
| `bypass` | Admin login bypass testing |
| `paths` | Directory listing finder |
| `httpfinger` | HTTP fingerprinting |
| `portscan` | Port scanner |
| `encode` | Encode/decode utilities (subcommands: b64, hex, url, bin, ascii) |
| `md5` | MD5 hash encoding |
| `crack` | MD5 hash cracking via online services |

### Core Functions

```python
def scan_panel(url: str, count: int = 3) -> list[str]:
    """Scan for admin login panels.

    Scans the target URL for known admin panel paths.

    Args:
        url: Target URL base (e.g., http://example.com)
        count: Maximum number of panels to find before stopping

    Returns:
        List of found admin panel URLs

    Raises:
        ValueError: If url is invalid or malformed
        requests.RequestException: On network errors
    """

def scan_sqli(url: str) -> bool:
    """Scan for SQL injection vulnerability.

    Tests the URL for SQL injection by injecting
    common SQL error-generating payloads.

    Args:
        url: Target URL with parameter

    Returns:
        True if SQLi vulnerability detected, False otherwise
    """

def scan_lfi(url: str, files: list[str] | None = None) -> list[str]:
    """Scan for LFI vulnerabilities.

    Tests the URL path parameter for local file inclusion.

    Args:
        url: Target URL with parameter
        files: Optional custom file list, defaults to common paths

    Returns:
        List of sensitive files accessible
    """

def scan_xss(url: str) -> list[dict[str, Any]]:
    """Scan for XSS vulnerabilities.

    Parses forms and tests for Reflected XSS.

    Args:
        url: Target URL

    Returns:
        List of dicts with vulnerable forms/params
    """

def scan_bypass(url: str, positive: str | None = None) -> str | None:
    """Try to bypass admin login.

    Tests common SQL injection bypass payloads.

    Args:
        url: Target login URL
        positive: String that appears on successful login

    Returns:
        Bypass payload that worked, or None
    """

def find_paths(url: str, full: bool = False) -> list[str]:
    """Find directory listings.

    Scans for 'Index of' directory listings.

    Args:
        url: Target URL
        full: Do full recursive scan

    Returns:
        List of directories with listing enabled
    """

def http_fingerprint(url: str) -> dict[str, str]:
    """Get HTTP server fingerprint.

    Args:
        url: Target URL

    Returns:
        Dict with server info (server, date, content_type, connection)
    """

def port_scan(ip: str, ports: list[int] | None = None) -> dict[int, str]:
    """Scan ports.

    Args:
        ip: Target IP
        ports: Optional port list, defaults to common ports

    Returns:
        Dict of open ports -> service name
    """

def encode_md5(text: str) -> str:
    """MD5 encode text.

    Args:
        text: Text to encode

    Returns:
        MD5 hash (32 hex characters)
    """

def crack_md5(hash: str) -> str | None:
    """Attempt to crack MD5 hash via online services.

    Args:
        hash: 32-character MD5 hash

    Returns:
        Decrypted hash or None if not found
    """

# Encoder functions
def encode_base64(text: str) -> str
def decode_base64(text: str) -> str
def encode_hex(text: str) -> str
def decode_hex(text: str) -> str
def encode_url(text: str) -> str
def decode_url(text: str) -> str
def text_to_bin(text: str) -> str
def bin_to_text(binary: str) -> str
def ascii_encode(text: str) -> str
def ascii_decode(codes: str) -> str
```

## Data Formats
- Wordlists: Plain text files with one entry per line
- Logs: Text files in `logs/` directory
- Payloads: SQL injection, XSS, LFI path lists embedded as module constants

## Edge Cases
- Invalid URLs should raise ValueError
- Network timeouts should return empty results, not crash
- Empty responses from servers should be handled
- WAF/IPS detection should be logged
- Form-based auth vs HTTP auth detection

## Performance & Constraints
- Default timeout: 10 seconds
- Rate limiting: Sequential requests, no concurrency by default
- Maximum panels to find: configurable (default 3)
- Maximum LFI files tested before stop: all in list