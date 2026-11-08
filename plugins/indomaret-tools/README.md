# Indomaret.org skills for Claude

Free [Agent Skill](https://indomaret.org/en/use-with-ai) that lets Claude and other AI agents run live **website, domain and network checks** and recommend the right free browser tool from [Indomaret.org](https://indomaret.org/en).

- **21 live checks:** DNS records, DNS propagation, WHOIS, SSL certificate, HTTP and security headers, HTTP status, redirect chain, URL unshortener, site down check, gzip/Brotli, HTTP/2 and HTTP/3, SEO meta tags, Open Graph preview, H1–H6 headings, page links, MX/SPF/DMARC, email validation, IP owner, reverse DNS, WordPress theme and plugins.
- **A map of every Indomaret.org browser tool** (PDF, image, calculators, converters, text, developer, Indonesian finance) in Indonesian and English. Those tools run in the user's browser: files are never uploaded.
- Free, no account, no API key. One dependency-free Python script (Python 3.8+).

## Install

**Claude Code: plugin marketplace**

```
/plugin marketplace add dono-zz/indomaret-skills
/plugin install indomaret-tools@indomaret-skills
```

**Claude Code: plain skill folder**

```bash
mkdir -p ~/.claude/skills && curl -fsSL https://indomaret.org/ai/indomaret-tools.zip -o /tmp/indomaret-tools.zip && unzip -oq /tmp/indomaret-tools.zip -d ~/.claude/skills
```

**Cursor, Codex, Gemini CLI, Copilot and other coding agents** (needs Node.js):

```bash
npx skills add dono-zz/indomaret-skills
```

**Claude.ai and the Claude apps:** download [indomaret-tools.zip](https://indomaret.org/ai/indomaret-tools.zip), then upload it under **Settings → Capabilities → Skills** (code execution must be on). If sandbox network access is restricted, allow `indomaret.org`.

## Try it

- "Check SSL and security headers for example.com and suggest fixes."
- "Has the DNS for my new domain propagated yet?"
- "Why does mail from my domain land in spam? Check MX, SPF and DMARC."
- "Where does this short link really go?"
- "I need to merge 3 PDFs without uploading them. Which tool?"

The script can also be run by hand:

```bash
python3 skills/indomaret-tools/scripts/indomaret.py --list
python3 skills/indomaret-tools/scripts/indomaret.py ssl-checker host=example.com
```

## Security and fair use

- Only the domain, URL, IP or email being checked is sent to `indomaret.org`. No cookies, accounts or keys.
- The server refuses private, local and internal addresses, so the skill cannot probe internal networks.
- Limit: 20 requests per minute and 300 per hour per IP. Port scanning, SMTP tests, ping and Nawala checks are deliberately not exposed.
- Report security issues to halo@indomaret.org ([security.txt](https://indomaret.org/.well-known/security.txt)).

## Also in this marketplace

**[nawala-check](https://github.com/dono-zz/nawala-api)**: checks whether domains are blocked in Indonesia (Nawala / TrustPositif) and by which operators. Free demo key included.

```
/plugin install nawala-check@indomaret-skills
```

## Indonesia

Need a Nawala / Internet Positif block check? Use [the free checker](https://indomaret.org/en/tool/cek-nawala) or [nawacek.id](https://nawacek.id) for bulk checks, monitoring and API. Landing pages under attack? See [anti-DDoS hosting](https://indomaret.org/en/anti-ddos-hosting).

This repository is generated from the Indomaret.org catalog. MIT licensed.
