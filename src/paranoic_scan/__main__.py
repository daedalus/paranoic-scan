"""CLI entry point."""

from __future__ import annotations

import click

from paranoic_scan import (
    crack_md5,
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
from paranoic_scan.encode import (
    ascii_decode,
    ascii_encode,
    bin_to_text,
    decode_base64,
    decode_hex,
    decode_url,
    encode_base64,
    encode_hex,
    encode_url,
    text_to_bin,
)


@click.group()
def main() -> None:
    """Paranoic Scan - Web security assessment tool."""
    pass


@main.command()
@click.argument("url")
@click.option("--count", default=3, help="Max panels to find")
def panel(url: str, count: int) -> None:
    """Find admin login panels."""
    click.echo(f"[+] Scanning {url} ...")
    found = scan_panel(url, count)
    if found:
        for p in found:
            click.echo(f"[+] Panel found: {p}")
    else:
        click.echo("[-] No panels found")


@main.command()
@click.argument("url")
def sqli(url: str) -> None:
    """Scan for SQL injection."""
    click.echo(f"[+] Scanning {url} ...")
    if scan_sqli(url):
        click.echo("[+] SQLi vulnerability detected!")
    else:
        click.echo("[-] No SQLi detected")


@main.command()
@click.argument("url")
def lfi(url: str) -> None:
    """Scan for LFI vulnerabilities."""
    click.echo(f"[+] Scanning {url} ...")
    found = scan_lfi(url)
    if found:
        for f in found:
            click.echo(f"[+] File accessible: {f}")
    else:
        click.echo("[-] No LFI detected")


@main.command()
@click.argument("url")
def xss(url: str) -> None:
    """Scan for XSS vulnerabilities."""
    click.echo(f"[+] Scanning {url} ...")
    found = scan_xss(url)
    if found:
        for v in found:
            click.echo(f"[+] XSS in form {v['form_index']}: {v['action']}")
    else:
        click.echo("[-] No XSS detected")


@main.command()
@click.argument("url")
def bypass(url: str) -> None:
    """Try admin login bypass."""
    click.echo(f"[+] Trying bypass on {url} ...")
    result = scan_bypass(url)
    if result:
        click.echo(f"[+] Bypass payload: {result}")
    else:
        click.echo("[-] Bypass failed")


@main.command()
@click.argument("url")
@click.option("--full", is_flag=True, help="Full recursive scan")
def paths(url: str, full: bool) -> None:
    """Find directory listings."""
    click.echo(f"[+] Scanning {url} ...")
    found = find_paths(url, full)
    if found:
        for p in found:
            click.echo(f"[+] Directory found: {p}")
    else:
        click.echo("[-] No directories found")


@main.command()
@click.argument("url")
def httpfinger(url: str) -> None:
    """HTTP fingerprint."""
    click.echo("[+] Getting fingerprint ...")
    info = http_fingerprint(url)
    for key, value in info.items():
        click.echo(f"[+] {key}: {value}")


@main.command()
@click.argument("ip")
@click.option("--ports", default="21,22,25,80,110,3306", help="Ports to scan")
def portscan(ip: str, ports: str) -> None:
    """Scan ports."""
    port_list = [int(p) for p in ports.split(",")]
    click.echo(f"[+] Scanning {ip} ...")
    open_ports = port_scan(ip, port_list)
    if open_ports:
        for port, service in open_ports.items():
            click.echo(f"[+] Port {port}: {service}")
    else:
        click.echo("[-] No open ports found")


@main.command()
@click.argument("text")
def md5(text: str) -> None:
    """MD5 encode text."""
    result = encode_md5(text)
    click.echo(f"[+] MD5: {result}")


@main.command()
@click.argument("hash")
def crack(hash: str) -> None:
    """Crack MD5 hash."""
    click.echo(f"[+] Cracking {hash} ...")
    result = crack_md5(hash)
    if result:
        click.echo(f"[+] Cracked: {result}")
    else:
        click.echo("[-] Not found")


encode_group = click.Group("encode")


@encode_group.command(name="b64")
@click.argument("text")
def b64(text: str) -> None:
    """Base64 encode."""
    click.echo(encode_base64(text))


@encode_group.command(name="b64d")
@click.argument("text")
def b64d(text: str) -> None:
    """Base64 decode."""
    click.echo(decode_base64(text))


@encode_group.command(name="hex")
@click.argument("text")
def hexenc(text: str) -> None:
    """Hex encode."""
    click.echo(encode_hex(text))


@encode_group.command(name="hexd")
@click.argument("text")
def hexdec(text: str) -> None:
    """Hex decode."""
    click.echo(decode_hex(text))


@encode_group.command(name="url")
@click.argument("text")
def urlenc(text: str) -> None:
    """URL encode."""
    click.echo(encode_url(text))


@encode_group.command(name="urld")
@click.argument("text")
def urldec(text: str) -> None:
    """URL decode."""
    click.echo(decode_url(text))


@encode_group.command(name="bin")
@click.argument("text")
def binenc(text: str) -> None:
    """Text to binary."""
    click.echo(text_to_bin(text))


@encode_group.command(name="bind")
@click.argument("binary")
def bindec(binary: str) -> None:
    """Binary to text."""
    click.echo(bin_to_text(binary))


@encode_group.command(name="ascii")
@click.argument("text")
def ascii(text: str) -> None:
    """ASCII encode."""
    click.echo(ascii_encode(text))


@encode_group.command(name="asciid")
@click.argument("codes")
def asciidec(codes: str) -> None:
    """ASCII decode."""
    click.echo(ascii_decode(codes))


main.add_command(encode_group)


if __name__ == "__main__":
    raise SystemExit(main())
