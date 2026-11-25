[![Update blocklist](https://github.com/EriusCalrissian/BlocklistDedupe/actions/workflows/update-blocklist.yml/badge.svg)](https://github.com/EriusCalrissian/BlocklistDedupe/actions/workflows/update-blocklist.yml)
# BlocklistDedupe

Merges several DNS blocklists into a single deduplicated list for [AdGuard Home](https://github.com/AdguardTeam/AdGuardHome) using [HostlistCompiler](https://github.com/AdguardTeam/HostlistCompiler). A GitHub Action rebuilds the list daily and commits it to [`dist/blocklist-main.txt`](dist/blocklist-main.txt).

## Usage in AdGuard Home

Go to *Filters → DNS blocklists → Add blocklist → Add a custom list* and enter this URL:

```
https://raw.githubusercontent.com/EriusCalrissian/BlocklistDedupe/main/dist/blocklist-main.txt
```

Afterwards you can remove the individual source lists from AdGuard Home.

## Reduction

Updated automatically on every build.

<!-- stats:start -->
| | Rules |
| --- | ---: |
| Sum of all sources | 724,470 |
| Merged list | **487,211** |
| Removed (duplicates, redundant subdomains, exclusions) | 237,259 (**32.7%**) |
<!-- stats:end -->

## Included sources

Generated automatically from [`configuration.json`](configuration.json) on every build.

<!-- sources:start -->
| Source | Format | Rules |
| --- | --- | ---: |
| [oisd big](https://big.oisd.nl) | adblock | 221,614 |
| [Stalkerware Indicators List](https://raw.githubusercontent.com/AdguardTeam/HostlistsRegistry/refs/heads/main/filters/security/filter_31_StalkerwareIndicatorsList/filter.txt) | adblock | 929 |
| [Complete Encrypted DNS Bypass Blocklist - incl. dnsbunker.org](https://raw.githubusercontent.com/EriusCalrissian/complete-doh-vpn-proxy-bypass-blocklist/main/adblock/doh.txt) | adblock | 3,558 |
| [AntiMalwareAdGuardHome.txt](https://raw.githubusercontent.com/DandelionSprout/adfilt/refs/heads/master/Alternate%20versions%20Anti-Malware%20List/AntiMalwareAdGuardHome.txt) | adblock | 12,564 |
| [HaGeZi's DynDNS - guards against dynamic DNS abuse!](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/dyndns.txt) | adblock | 1,497 |
| [HaGeZi's Badware Hoster - guards against malicious hosting services!](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/hoster.txt) | adblock | 1,266 |
| [HaGeZi's Amazon Tracker - blocks built-in trackers from devices, apps, and OSes!](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.amazon.txt) | adblock | 381 |
| [HaGeZi's Apple Tracker - blocks built-in trackers from devices, apps, and OSes!](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.apple.txt) | adblock | 106 |
| [HaGeZi's Huawei Tracker - blocks built-in trackers from devices, apps, and OSes!](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.huawei.txt) | adblock | 149 |
| [HaGeZi's OPPO & Realme Tracker - blocks built-in trackers from devices, apps, and OSes!](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.oppo-realme.txt) | adblock | 533 |
| [HaGeZi's Samsung Tracker - blocks built-in trackers from devices, apps, and OSes!](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.samsung.txt) | adblock | 202 |
| [HaGeZi's TikTok Tracker - blocks built-in trackers from devices, apps, and OSes!](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.tiktok.txt) | adblock | 554 |
| [HaGeZi's Microsoft Tracker - blocks built-in trackers from devices, apps, and OSes!](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.winoffice.txt) | adblock | 396 |
| [HaGeZi's Xiaomi Tracker - blocks built-in trackers from devices, apps, and OSes!](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.xiaomi.txt) | adblock | 412 |
| [HaGeZi's Multi PRO - extended protection (recommended)](https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.txt) | adblock | 246,434 |
| [HaGeZi's Threat Intelligence Feeds - medium version (best for browser/mobile ad blockers)](https://raw.githubusercontent.com/hagezi/dns-blocklists/refs/heads/main/adblock/tif.medium.txt) | adblock | 233,875 |
<!-- sources:end -->

## Managing sources

All sources are listed under `sources` in [`configuration.json`](configuration.json).

- **Add:** append an entry, e.g.
  ```json
  { "source": "https://example.org/list.txt", "type": "adblock" }
  ```
  Use `"type": "hosts"` for lists in `/etc/hosts` format.
- **Name (optional):** the [source table](#included-sources) uses the list's own `! Title:` (or `# Title:`) header. Set `"name": "My list"` to override it. Without either, the file name from the URL is shown.
- **Remove:** delete the entry.
- **Never block a domain:** add it to [`exclusions.txt`](exclusions.txt).

## How the build works

The workflow in [`.github/workflows/update-blocklist.yml`](.github/workflows/update-blocklist.yml) runs:

- daily at 06:00 UTC,
- on every push to `main` that changes `configuration.json`, `exclusions.txt`, `scripts/update_stats.py` or the workflow itself,
- manually via *Actions → Update blocklist → Run workflow*.

It compiles all sources, refreshes the [reduction stats](#reduction) and [source table](#included-sources) above with [`scripts/update_stats.py`](scripts/update_stats.py), then commits the result with [git-auto-commit-action](https://github.com/stefanzweifel/git-auto-commit-action) only if the rules actually changed (header timestamps are ignored). If the build yields fewer than 1000 rules, for example because sources are unreachable, it fails and the existing list stays in place.

## Setup for a fork

1. Fork the repository (it must be **public** for the raw URLs to work).
2. If the commit step fails with a 403 error, enable *Settings → Actions → General → Workflow permissions → Read and write permissions*.
3. Run the workflow once manually to create `dist/blocklist-main.txt`.

## License

See [`LICENSE`](LICENSE).
