# paranoic-scan

Web security assessment tool for self-auditing web applications. Based on Paranoic Scan 1.7 (2014) by Doddy Hackman - modernized to Python with updated security patterns.

**Note:** This tool is based on a 2014 Perl tool and is intended for authorized security testing on systems you own or have permission to test. The vulnerability detection techniques may be outdated for modern applications with WAF/IPS protection.

[![PyPI](https://img.shields.io/pypi/v/paranoic-scan.svg)](https://pypi.org/project/paranoic-scan/)
[![Python](https://img.shields.io/pypi/pyversions/paranoic-scan.svg)](https://pypi.org/project/paranoic-scan/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Install

```bash
pip install paranoic-scan
```

## Usage

```bash
# Find admin panels
paranoic-scan panel http://example.com

# Scan for SQL injection
paranoic-scan sqli http://example.com/page?id=1

# Scan for LFI
paranoic-scan lfi http://example.com/view?file=

# Scan for XSS
paranoic-scan xss http://example.com/search?q=

# Try admin login bypass
paranoic-scan bypass http://example.com/admin/login

# Find directory listings
paranoic-scan paths http://example.com

# HTTP fingerprinting
paranoic-scan httpfinger http://example.com

# Port scan
paranoic-scan portscan 192.168.1.1

# MD5 encode
paranoic-scan md5 "password"

# MD5 crack
paranoic-scan crack 098f6bcd4621d373cade4e832627b4f6

# Encoder utilities
paranoic-scan encode b64 "text"
paranoic-scan encode hex "text"
paranoic-scan encode url "text"
paranoic-scan encode bin "text"
paranoic-scan encode ascii "text"
```

## CLI

```bash
paranoic-scan --help
```

## API

```python
from paranoic_scan import (
    scan_panel,
    scan_sqli,
    scan_lfi,
    scan_xss,
    encode_md5,
)

# Find admin panels
panels = scan_panel("http://example.com", count=5)

# Scan for SQLi
is_vulnerable = scan_sqli("http://example.com?id=1")

# Encode MD5
hash = encode_md5("password")
```

## Development

```bash
git clone https://github.com/daedalus/paranoic-scan.git
cd paranoic-scan
pip install -e ".[test]"

# run tests
pytest

# format
ruff format src/ tests/

# lint
ruff check src/ tests/

# type check
mypy src/
```

## Disclaimer

This tool is provided for authorized security testing only. Use only on systems you own or have explicit written permission to test. The author is not responsible for any misuse or damage caused by this tool.