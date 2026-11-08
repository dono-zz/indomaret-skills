# nawala-check

Claude plugin that checks whether domains are **blocked in Indonesia** (Nawala, Internet Positif, TrustPositif) by Komdigi (formerly Kominfo) and 11 providers: Telkomsel, Indosat Ooredoo, XL Axiata, Axis, Three, Smartfren, IDNIC, iForte, Lintasarta and more.

Ask Claude things like *"Is example.com blocked in Indonesia?"* or *"Cek apakah domain-domain ini kena Nawala"*. The skill runs one dependency-free Python script and reports, per domain, whether it is blocked and by which operators.

- Uses the shared free demo key (100 requests per day for all demo users). It never reads credentials from your machine.
- Have a paid key? Give it to Claude in the conversation and it passes it with `--key`.
- Domains you check are sent to the Nawala API at `epiai.h80.org` (operated by nawacek.id). Results are cached for 5 minutes.

Paid plan: Rp 7.500.000 per month, 10,000 requests per day, up to 10 domains per request. Docs: [nawacek.id/api-nawala](https://nawacek.id/api-nawala). Order on Telegram [@gembels](https://t.me/gembels).

API docs and code examples: [github.com/dono-zz/nawala-api](https://github.com/dono-zz/nawala-api). MIT licensed.
