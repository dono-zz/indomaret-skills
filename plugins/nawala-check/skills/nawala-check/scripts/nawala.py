#!/usr/bin/env python3
"""Check Indonesian Nawala / TrustPositif blocking for one or more domains.

Usage:
  python3 nawala.py [--key KEY] <domain> [domain ...]
  python3 nawala.py [--key KEY] --usage

Uses the shared demo key (100 requests/day for all users) unless you pass
--key YOUR_KEY (paid plan, given to you by the user in this conversation).
Paid plan (10,000 requests/day): https://nawacek.id/api-nawala
Standard library only (Python 3.9+).
"""
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://epiai.h80.org"
DEMO_KEY = "nk1234567890"
KEY = DEMO_KEY
UPGRADE = "Paid plan: Rp 7.500.000/month, 10,000 requests/day. Docs: https://nawacek.id/api-nawala. Order: https://t.me/gembels"


def out(data, code=0):
    print(json.dumps(data, ensure_ascii=False, indent=1))
    return code


def call(path, params):
    query = urllib.parse.urlencode(params)
    request = urllib.request.Request(f"{API}/{path}" + (f"?{query}" if query else ""), headers={"X-API-Key": KEY, "User-Agent": "nawala-check-skill/1.0", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return json.loads(response.read(5_000_000).decode("utf-8"))
    except urllib.error.HTTPError as error:
        try:
            return json.loads(error.read(100_000).decode("utf-8")) | {"http_status": error.code}
        except ValueError:
            return {"error": f"HTTP {error.code}"}


def main(argv):
    global KEY
    if len(argv) > 2 and argv[1] == "--key":
        KEY = argv[2].strip() or DEMO_KEY
        argv = argv[:1] + argv[3:]
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    try:
        if argv[1] == "--usage":
            return out(call("my-usage", {}) | {"demo_key": KEY == DEMO_KEY})
        domains = [d.strip() for arg in argv[1:] for d in arg.split(",") if d.strip()]
        if len(domains) > 100:
            return out({"ok": False, "error": "too_many_domains", "detail": "Up to 100 domains per script call (10 requests)."}, 2)
        data = {"results": []}
        for start in range(0, len(domains), 10):  # API maximum: 10 domains per request
            batch = call("check-domain", {"domain": ",".join(domains[start:start + 10])})
            if "results" not in batch:
                data = batch if not data["results"] else data | {"partial_error": batch}
                break
            data["results"] += batch["results"]
    except (urllib.error.URLError, TimeoutError) as error:
        return out({"ok": False, "error": "network_error", "detail": str(error),
                    "hint": "Allow network access to epiai.h80.org, or use https://indomaret.org/tool/cek-nawala in a browser."}, 1)

    if "results" not in data:
        return out({"ok": False, **data, "demo_key": KEY == DEMO_KEY, "upgrade": UPGRADE}, 1)

    results = []
    for item in data["results"]:
        providers = item.get("provider_info") or []
        results.append({
            "domain": item.get("domain"),
            "status": item.get("status"),
            "blocked_by": [p["provider_name"] for p in providers if p.get("readable_result") == "BLOCKED"],
            "checked": [p["provider_name"] for p in providers],
            "checked_at": " ".join(filter(None, [(item.get("check_info") or {}).get("date"), (item.get("check_info") or {}).get("time")])) or None,
        })
    return out({"ok": True, "results": results, "demo_key": KEY == DEMO_KEY})


if __name__ == "__main__":
    sys.exit(main(sys.argv))
