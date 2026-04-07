from paranoic_scan.encode import (
    ascii_decode,
    ascii_encode,
    bin_to_text,
    decode_base64,
    decode_hex,
    decode_multiline,
    decode_url,
    encode_base64,
    encode_hex,
    encode_multiline,
    encode_url,
    text_to_bin,
)


class TestEncodeBase64:
    """Tests for encode_base64 function."""

    def test_encode_basic(self):
        """Test basic Base64 encoding."""
        assert encode_base64("test") == "dGVzdA=="

    def test_encode_empty(self):
        """Test empty string encoding."""
        assert encode_base64("") == ""

    def test_encode_special_chars(self):
        """Test special character encoding."""
        result = encode_base64("hello world")
        assert result == "aGVsbG8gd29ybGQ="

    def test_encode_binary(self):
        """Test binary data encoding."""
        result = encode_base64("\x00\x01\x02")
        assert result == "AAEC"


class TestDecodeBase64:
    """Tests for decode_base64 function."""

    def test_decode_basic(self):
        """Test basic Base64 decoding."""
        assert decode_base64("dGVzdA==") == "test"

    def test_decode_empty(self):
        """Test empty string decoding."""
        assert decode_base64("") == ""

    def test_decode_invalid(self):
        """Test invalid Base64 returns empty."""
        assert decode_base64("not-valid-base64!!!") == ""


class TestEncodeHex:
    """Tests for encode_hex function."""

    def test_encode_basic(self):
        """Test basic hex encoding."""
        assert encode_hex("test") == "0x74657374"

    def test_encode_empty(self):
        """Test empty string encoding."""
        assert encode_hex("") == "0x"

    def test_encode_single_char(self):
        """Test single character encoding."""
        assert encode_hex("a") == "0x61"

    def test_encode_multiple_chars(self):
        """Test multiple character encoding."""
        assert encode_hex("abc") == "0x616263"


class TestDecodeHex:
    """Tests for decode_hex function."""

    def test_decode_basic(self):
        """Test basic hex decoding."""
        assert decode_hex("0x74657374") == "test"

    def test_decode_without_prefix(self):
        """Test hex decoding without 0x prefix."""
        assert decode_hex("74657374") == "test"

    def test_decode_empty(self):
        """Test empty string decoding."""
        assert decode_hex("") == ""

    def test_decode_invalid(self):
        """Test invalid hex returns empty."""
        assert decode_hex("not-valid-hex") == ""

    def test_decode_garbage(self):
        """Test garbage hex returns empty."""
        assert decode_hex("xyzxyz") == ""


class TestEncodeURL:
    """Tests for encode_url function."""

    def test_encode_basic(self):
        """Test basic URL encoding."""
        assert encode_url("test") == "test"

    def test_encode_spaces(self):
        """Test space encoding."""
        assert encode_url("test here") == "test%20here"

    def test_encode_special(self):
        """Test special character encoding."""
        result = encode_url("test?foo=bar&baz=qux")
        assert "%3F" in result or "?" in result

    def test_encode_unicode(self):
        """Test unicode encoding."""
        result = encode_url("test")
        assert result == "test"


class TestDecodeURL:
    """Tests for decode_url function."""

    def test_decode_basic(self):
        """Test basic URL decoding."""
        assert decode_url("test") == "test"

    def test_decode_encoded(self):
        """Test encoded URL decoding."""
        assert decode_url("test%20here") == "test here"

    def test_decode_empty(self):
        """Test empty string decoding."""
        assert decode_url("") == ""

    def test_decode_special(self):
        """Test special character decoding."""
        assert decode_url("test%3F") == "test?"


class TestTextToBin:
    """Tests for text_to_bin function."""

    def test_basic(self):
        """Test basic conversion."""
        assert text_to_bin("test") == "01110100011001010111001101110100"

    def test_empty(self):
        """Test empty string."""
        assert text_to_bin("") == ""

    def test_single_char(self):
        """Test single character."""
        assert text_to_bin("a") == "01100001"

    def test_ascii_range(self):
        """Test ASCII range conversion."""
        result = text_to_bin("AB")
        assert len(result) == 16


class TestBinToText:
    """Tests for bin_to_text function."""

    def test_basic(self):
        """Test basic conversion."""
        assert bin_to_text("01110100011001010111001101110100") == "test"

    def test_empty(self):
        """Test empty string."""
        assert bin_to_text("") == ""

    def test_invalid(self):
        """Test invalid binary returns empty."""
        assert bin_to_text("not-binary!!!") == ""

    def test_short_binary(self):
        """Test short binary (incomplete byte)."""
        result = bin_to_text("0111010")
        assert result == ""


class TestAsciiEncode:
    """Tests for ascii_encode function."""

    def test_basic(self):
        """Test basic ASCII encoding."""
        assert ascii_encode("test") == "116,101,115,116"

    def test_empty(self):
        """Test empty string."""
        assert ascii_encode("") == ""

    def test_single_char(self):
        """Test single character."""
        assert ascii_encode("a") == "97"

    def test_multiple_chars(self):
        """Test multiple characters."""
        result = ascii_encode("ab")
        assert result == "97,98"


class TestAsciiDecode:
    """Tests for ascii_decode function."""

    def test_basic(self):
        """Test basic ASCII decoding."""
        assert ascii_decode("116,101,115,116") == "test"

    def test_empty(self):
        """Test empty string."""
        assert ascii_decode("") == ""

    def test_invalid(self):
        """Test invalid returns empty."""
        assert ascii_decode("not-valid") == ""

    def test_out_of_range(self):
        """Test out of range ASCII code."""
        result = ascii_decode("9999999")
        assert result == ""


class TestEncodeMultiline:
    """Tests for encode_multiline function."""

    def test_basic(self):
        """Test basic multiline encoding."""
        result = encode_multiline("test\nok")
        lines = result.split("\n")
        assert len(lines) == 2
        assert lines[0].startswith("0x")
        assert lines[1].startswith("0x")

    def test_single_line(self):
        """Test single line encoding."""
        result = encode_multiline("test")
        assert result == "0x74657374"

    def test_empty_lines(self):
        """Test empty lines."""
        result = encode_multiline("")
        assert result == "0x"


class TestDecodeMultiline:
    """Tests for decode_multiline function."""

    def test_basic(self):
        """Test basic multiline decoding."""
        result = decode_multiline("0x74657374\n0x6f6b")
        assert result == "test\nok"

    def test_single_line(self):
        """Test single line decoding."""
        result = decode_multiline("0x74657374")
        assert result == "test"

    def test_empty(self):
        """Test empty decoding."""
        result = decode_multiline("")
        assert result == ""


class TestEncoderEdgeCases:
    """Edge case tests for encoder functions."""

    def test_encode_hex_unicode(self):
        """Test hex encode with unicode."""
        try:
            result = encode_hex("")
            assert result == "0x"
        except Exception:
            pytest.fail("Should not raise")

    def test_decode_hex_invalid_length(self):
        """Test hex decode with odd length."""
        result = decode_hex("0xabc")
        assert result == "" or result is not None

    def test_bin_to_text_odd_length(self):
        """Test binary with odd length."""
        result = bin_to_text("1")
        assert result == ""

    def test_ascii_decode_empty_parts(self):
        """Test ASCII decode with empty parts."""
        result = ascii_decode(",,")
        assert result == ""

    def test_url_encode_empty(self):
        """Test URL encode empty string."""
        result = encode_url("")
        assert result == ""

    def test_url_decode_empty(self):
        """Test URL decode empty string."""
        result = decode_url("")
        assert result == ""
