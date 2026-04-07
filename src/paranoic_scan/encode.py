"""Encoder/decoder utilities.

This module provides various encoding and decoding functions useful for
security testing including Base64, Hex, URL, Binary, and ASCII conversions.

Example:
    >>> from paranoic_scan import encode_base64
    >>> encode_base64("test")
    'dGVzdA=='
"""

from __future__ import annotations

import base64
import binascii
import urllib.parse


def encode_base64(text: str) -> str:
    """Base64 encode text.

    Args:
        text: Text to encode

    Returns:
        Base64 encoded string

    Example:
        >>> encode_base64("test")
        'dGVzdA=='
    """
    return base64.b64encode(text.encode()).decode()


def decode_base64(text: str) -> str:
    """Base64 decode text.

    Args:
        text: Base64 encoded string

    Returns:
        Decoded string, empty string on error

    Example:
        >>> decode_base64("dGVzdA==")
        'test'
    """
    try:
        return base64.b64decode(text.encode()).decode()
    except binascii.Error:
        return ""


def encode_hex(text: str) -> str:
    """Hex encode text.

    Args:
        text: Text to encode

    Returns:
        Hex encoded string with 0x prefix

    Example:
        >>> encode_hex("test")
        '0x74657374'
    """
    result = "0x"
    for c in text:
        result = result + f"{ord(c):02x}"
    return result


def decode_hex(text: str) -> str:
    """Hex decode text.

    Args:
        text: Hex string (with or without 0x prefix)

    Returns:
        Decoded string, empty string on error

    Example:
        >>> decode_hex("0x74657374")
        'test'
    """
    hex_str = text
    if hex_str.startswith("0x"):
        hex_str = hex_str[2:]
    try:
        return bytes.fromhex(hex_str).decode()
    except (ValueError, UnicodeDecodeError):
        return ""


def encode_url(text: str) -> str:
    """URL encode text.

    Args:
        text: Text to encode

    Returns:
        URL encoded string

    Example:
        >>> encode_url("test here")
        'test%20here'
    """
    return urllib.parse.quote(text)


def decode_url(text: str) -> str:
    """URL decode text.

    Args:
        text: URL encoded string

    Returns:
        Decoded string

    Example:
        >>> decode_url("test%20here")
        'test here'
    """
    return urllib.parse.unquote(text)


def text_to_bin(text: str) -> str:
    """Convert text to binary.

    Args:
        text: Text to convert

    Returns:
        Binary string (8 bits per character)

    Example:
        >>> text_to_bin("test")
        '01110100011001010111001101110100'
    """
    result = ""
    for c in text:
        result = result + f"{ord(c):08b}"
    return result


def bin_to_text(binary: str) -> str:
    """Convert binary to text.

    Args:
        binary: Binary string (8 bits per character)

    Returns:
        Text string, empty string on error

    Example:
        >>> bin_to_text("01110100011001010111001101110100")
        'test'
    """
    result = ""
    try:
        i = 0
        while i < len(binary):
            chunk = binary[i : i + 8]
            if len(chunk) != 8:
                return ""
            result = result + chr(int(chunk, 2))
            i = i + 8
    except (ValueError, UnicodeDecodeError):
        return ""
    return result


def ascii_encode(text: str) -> str:
    """Convert text to ASCII codes.

    Args:
        text: Text to convert

    Returns:
        Comma-separated ASCII codes

    Example:
        >>> ascii_encode("test")
        '116,101,115,116'
    """
    parts = []
    for c in text:
        parts.append(str(ord(c)))
    return ",".join(parts)


def ascii_decode(codes: str) -> str:
    """Convert ASCII codes to text.

    Args:
        codes: Comma-separated ASCII codes

    Returns:
        Text string, empty string on error

    Example:
        >>> ascii_decode("116,101,115,116")
        'test'
    """
    result = ""
    try:
        for c in codes.split(","):
            result = result + chr(int(c))
    except ValueError:
        return ""
    return result


def encode_multiline(text: str) -> str:
    """Encode multiline text.

    Args:
        text: Text to encode (may contain newlines)

    Returns:
        Encoded text with each line hex-encoded

    Example:
        >>> encode_multiline("test\\nok")
        '0x74657374\\n0x6f6b'
    """
    lines = text.split("\n")
    result_lines = []
    for line in lines:
        result_lines.append(encode_hex(line))
    return "\n".join(result_lines)


def decode_multiline(text: str) -> str:
    """Decode multiline encoded text.

    Args:
        text: Encoded text (each line hex-encoded)

    Returns:
        Decoded text

    Example:
        >>> decode_multiline("0x74657374\\n0x6f6b")
        'test\\nok'
    """
    lines = text.split("\n")
    result_lines = []
    for line in lines:
        result_lines.append(decode_hex(line))
    return "\n".join(result_lines)
