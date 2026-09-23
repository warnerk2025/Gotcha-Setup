# Gotcha-Setup

Gotcha-Setup is a ready-to-run Python OSINT utility for username and email reconnaissance. It includes async platform scanning, batch processing, TXT/JSON/CSV reporting, public breach lookups, domain analysis, and optional adult-platform checks behind an explicit `--adult` flag.

## Features

- Broad username reconnaissance across social, developer, gaming, forum, general, and adult platform definitions
- Email reconnaissance with local-part platform scanning, domain analysis, and public breach lookups
- Async concurrent scanning with configurable `--threads` and `--timeout`
- Batch processing from a newline-delimited input file
- JSON, CSV, and TXT report generation
- Adult/NSFW platform support only when `--adult` is supplied
- Graceful timeout/error handling so one failing site does not stop the scan

## Repository layout

```text
Gotcha-Setup/
├── main.py
├── requirements.txt
├── core/
│   ├── banner.py
│   ├── config.py
│   └── logger.py
├── engines/
│   ├── breach_checker.py
│   ├── email_hunter.py
│   ├── social_media.py
│   └── username_hunter.py
└── utils/
    ├── reporter.py
    └── validator.py
```

## Installation

```bash
git clone https://github.com/warnerk2025/Gotcha-Setup.git
cd Gotcha-Setup
python3 -m pip install -r requirements.txt
python3 main.py -h
```

If the help menu renders, the repository is ready to use.

## Usage

### Username scanning

```bash
python3 main.py -u octocat --social --developer
python3 main.py -u sample_user --all
python3 main.py -u sample_user --social --adult
```

### Email scanning

```bash
python3 main.py -e user@example.com --breaches --domain
python3 main.py -e user@example.com --social --general --developer --forums --gaming --professional --domain
python3 main.py -e user@example.com --all
```

### Batch processing

```bash
python3 main.py -f targets.txt --all -o reports/results.json --format json
python3 main.py -f targets.txt --social --developer -o reports/results.csv --format csv
python3 main.py -f targets.txt --breaches --domain -o reports/results.txt --format txt
```

## CLI options

- `-u, --username`: single username target
- `-e, --email`: single email target
- `-f, --file`: newline-delimited file of usernames and/or emails
- `--social`: social media checks (also tries the email local-part against social profiles)
- `--general`: general web profile checks (also tries the email local-part)
- `--developer`: developer platform checks (also tries the email local-part)
- `--forums`: forum/community checks (also tries the email local-part)
- `--gaming`: gaming profile checks (also tries the email local-part)
- `--breaches`: public breach lookup
- `--professional`: professional-network profile lookup based on the email local-part
- `--domain`: MX/NS/TXT/SPF/DMARC analysis for email domains
- `--adult`: opt in to adult/NSFW platform checks
- `--all`: enable all non-adult scan modules, including local-part platform scans for email targets
- `--threads`: maximum concurrent requests per scanning engine
- `--timeout`: per-request timeout in seconds
- `-o, --output`: save report to disk
- `--format`: `json`, `csv`, or `txt`
- `--quiet`: suppress the banner and most log output

## Breach lookups

The breach checker makes best-effort requests to the public XposedOrNot email endpoint. If you set `HIBP_API_KEY`, it will also query Have I Been Pwned's authenticated API. Results depend on those third-party services being reachable and continuing to support the same interfaces.

```bash
export HIBP_API_KEY="your_api_key"
python3 main.py -e user@example.com --breaches
```

Using `--breaches` sends the target email address to those third-party breach services so they can perform the lookup. Only enable that option when you are authorized to share the target email with external providers.

## Notes

- Adult platform definitions are excluded by default.
- Email platform scans reuse the email local-part only when it is a valid supported username.
- Public sites change often; a `possible`, `timeout`, or `error` status usually means the endpoint blocked automation or changed its routing.
- Use this tool responsibly and only against data you are authorized to investigate.
