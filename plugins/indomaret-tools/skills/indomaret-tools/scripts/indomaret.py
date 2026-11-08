#!/usr/bin/env python3
"""Run an Indomaret.org check and print its JSON result.

Usage:
  python3 indomaret.py <tool> host=<domain|url|ip|email> [key=value ...]
  python3 indomaret.py --list

Examples:
  python3 indomaret.py dns-lookup host=example.com type=MX
  python3 indomaret.py ssl-checker host=github.com
  python3 indomaret.py redirect-checker host=http://example.com

Only public hosts are accepted; the server refuses private and internal
addresses. Free, no API key. Limit: 20 requests/minute, 300/hour per IP.
Standard library only (Python 3.8+).
"""
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://indomaret.org"
VERSION = "1.1.0"
TOOLS = json.loads(r'''{
    "dns-lookup": {
        "params": {
            "host": "domain",
            "type": "ALL, A, AAAA, CNAME, MX, NS, TXT, SOA or CAA"
        },
        "about": "See every DNS record for a domain: A, AAAA, MX, NS, TXT, CNAME, SOA, CAA.",
        "page": "https://indomaret.org/en/tool/dns-lookup"
    },
    "dns-propagation-checker": {
        "params": {
            "host": "domain",
            "type": "A, AAAA, CNAME, MX, NS or TXT"
        },
        "about": "Ask 14 public resolvers for a domain’s DNS record at once and see which ones already serve the new data.",
        "page": "https://indomaret.org/en/tool/dns-propagation-checker"
    },
    "domain-whois": {
        "params": {
            "host": "domain"
        },
        "about": "Look up a domain’s WHOIS data: registrar, creation and expiry dates, nameservers and status.",
        "page": "https://indomaret.org/en/tool/domain-whois"
    },
    "hostname-to-ip": {
        "params": {
            "host": "hostname"
        },
        "about": "Find the IPv4 and IPv6 addresses of a domain or hostname, with TTLs.",
        "page": "https://indomaret.org/en/tool/hostname-to-ip"
    },
    "ip-to-hostname": {
        "params": {
            "host": "ip"
        },
        "about": "Find the hostname behind an IP address with a reverse DNS (PTR) lookup, IPv4 or IPv6.",
        "page": "https://indomaret.org/en/tool/ip-to-hostname"
    },
    "ip-information": {
        "params": {
            "host": "ip or domain"
        },
        "about": "Find out who owns an IP: ISP/organisation, ASN, country, network block and hostname.",
        "page": "https://indomaret.org/en/tool/ip-information"
    },
    "mx-lookup": {
        "params": {
            "host": "domain"
        },
        "about": "See a domain’s mail servers (MX) with priority and IPs, plus its SPF and DMARC records.",
        "page": "https://indomaret.org/en/tool/mx-lookup"
    },
    "email-validator": {
        "params": {
            "host": "email address"
        },
        "about": "Check an email address’s format and whether its domain can receive mail (MX), with typo hints.",
        "page": "https://indomaret.org/en/tool/email-validator"
    },
    "ssl-checker": {
        "params": {
            "host": "domain",
            "port": "optional, default 443"
        },
        "about": "Check a domain’s SSL/HTTPS certificate: validity, days until expiry, issuer and chain.",
        "page": "https://indomaret.org/en/tool/ssl-checker"
    },
    "http-headers-parser": {
        "params": {
            "host": "url",
            "follow": "true or false"
        },
        "about": "See the response headers of a URL (like curl -I) and audit its security headers.",
        "page": "https://indomaret.org/en/tool/http-headers-parser"
    },
    "http-status-code-checker": {
        "params": {
            "host": "url",
            "follow": "true or false"
        },
        "about": "Check a URL’s HTTP status code and what it means, including the final status after redirects.",
        "page": "https://indomaret.org/en/tool/http-status-code-checker"
    },
    "redirect-checker": {
        "params": {
            "host": "url"
        },
        "about": "See every redirect hop for a URL: status code, target, timing and the final destination.",
        "page": "https://indomaret.org/en/tool/redirect-checker"
    },
    "url-unshortener": {
        "params": {
            "host": "short url"
        },
        "about": "See where a short link really leads, without opening it on your device.",
        "page": "https://indomaret.org/en/tool/url-unshortener"
    },
    "website-status-checker": {
        "params": {
            "host": "url"
        },
        "about": "Check whether a site is down for everyone: HTTP status, response time and server IP, tested from our server.",
        "page": "https://indomaret.org/en/tool/website-status-checker"
    },
    "gzip-test": {
        "params": {
            "host": "url"
        },
        "about": "Check whether a web page is gzip/Brotli compressed and by what percentage it shrinks.",
        "page": "https://indomaret.org/en/tool/gzip-test"
    },
    "http2-checker": {
        "params": {
            "host": "url"
        },
        "about": "Check a website’s HTTP/2 support (via ALPN) and HTTP/3 advertisement (via Alt-Svc).",
        "page": "https://indomaret.org/en/tool/http2-checker"
    },
    "meta-tag-checker": {
        "params": {
            "host": "url"
        },
        "about": "Enter a URL to see all its SEO meta tags, with fixes and a Google result preview.",
        "page": "https://indomaret.org/en/tool/meta-tag-checker"
    },
    "open-graph-checker": {
        "params": {
            "host": "url"
        },
        "about": "See roughly how your link looks when shared, and why its image is missing.",
        "page": "https://indomaret.org/en/tool/open-graph-checker"
    },
    "heading-checker": {
        "params": {
            "host": "url"
        },
        "about": "Show a web page’s H1–H6 outline and spot missing, duplicate or skipped headings.",
        "page": "https://indomaret.org/en/tool/heading-checker"
    },
    "link-extractor": {
        "params": {
            "host": "url",
            "assets": "true or false"
        },
        "about": "List every link on a page with its anchor text and rel attributes, ready to download as CSV.",
        "page": "https://indomaret.org/en/tool/link-extractor"
    },
    "wordpress-theme-detector": {
        "params": {
            "host": "url"
        },
        "about": "Find out which WordPress theme and plugins a website uses, from its publicly visible traces.",
        "page": "https://indomaret.org/en/tool/wordpress-theme-detector"
    }
}''')
MAX_BYTES = 2_000_000


def out(data, code=0):
    print(json.dumps(data, ensure_ascii=False, indent=1))
    return code


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    if argv[1] == "--list":
        for slug, tool in TOOLS.items():
            params = " ".join(f"{k}=<{v}>" for k, v in tool["params"].items())
            print(f"{slug} {params}\n    {tool['about']}")
        return 0

    slug = argv[1]
    tool = TOOLS.get(slug)
    if tool is None:
        return out({"ok": False, "error": "unknown_tool", "tools": sorted(TOOLS)}, 2)

    params = {}
    for arg in argv[2:]:
        key, sep, value = arg.partition("=")
        if not sep or key not in tool["params"]:
            return out({"ok": False, "error": "unknown_param", "param": key, "allowed": sorted(tool["params"])}, 2)
        params[key] = value.strip()
    if not params.get("host"):
        return out({"ok": False, "error": "missing_param", "param": "host"}, 2)

    url = f"{BASE}/api/tool/{slug}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(url, headers={
        "User-Agent": f"indomaret-skill/{VERSION} (+{BASE}/en/use-with-ai)",
        "Accept": "application/json",
    })
    status = 200
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            body = response.read(MAX_BYTES)
    except urllib.error.HTTPError as error:
        status = error.code
        body = error.read(MAX_BYTES)
        if status == 429:
            return out({"ok": False, "error": "rate_limited", "detail": "Limit is 20 requests/minute and 300/hour. Wait, then retry once.", "retry_after": error.headers.get("Retry-After")}, 1)
    except (urllib.error.URLError, TimeoutError) as error:
        return out({"ok": False, "error": "network_error", "detail": str(error),
                    "hint": "If this runs in a sandbox, allow network access to indomaret.org, or open the tool page in a browser.",
                    "page": tool["page"]}, 1)

    try:
        data = json.loads(body.decode("utf-8"))
    except ValueError:
        return out({"ok": False, "error": "bad_response", "status": status, "page": tool["page"]}, 1)

    data["page"] = tool["page"]
    return out(data, 0 if data.get("ok") else 1)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
