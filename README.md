# crawler

---

**crawler** is a simple, domain-restricted web crawler written in Python.
It recursively follows and prints all discovered links within the same registered domain.
Designed for simplicity, clarity, and bug bounty / reconnaissance use cases.

---

# 🚀 Features

* Crawls all links from a starting URL (within the same domain)
* Prints each found link — one per line
* Optionally saves results to a file
* Auto-normalizes relative URLs
* Respects HTML-only targets
* Lightweight and dependency-minimal
* Gracefully handles interruptions (`Ctrl + C`)

---

##🧠 Example Output

```
[+] Started crawling for => https://www.ifood.com.br

https://www.ifood.com.br
https://www.ifood.com.br/restaurants
https://www.ifood.com.br/contact
...
```

---

# 🧩 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/crawler.git
cd crawler
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

# ⚙️ Usage

# Basic crawling

```bash
python crawler.py -u https://example.com
```

# Save results to a file

```bash
python crawler.py -u https://example.com -o links.txt
```

# Set custom delay between requests (default: 0.5s)

```bash
python crawler.py -u https://example.com -d 1
```

---

# 🧾 Arguments

| Flag             | Description                      | Required | Default |
| ---------------- | -------------------------------- | -------- | ------- |
| `-u`, `--url`    | Starting URL to crawl            | ✅        | —       |
| `-o`, `--output` | Output file to save links        | ❌        | None    |
| `-d`, `--delay`  | Delay between requests (seconds) | ❌        | 0.5     |

---

# 🧱 Dependencies

Listed in [`requirements.txt`](./requirements.txt):

```
requests
argparse
beautifulsoup4
parse
pyfiglet
tldextract
```

---

# 🧤 Example Use Case

Ideal for:

* Bug bounty reconnaissance
* Link mapping
* Content discovery
* Research on internal linking

---

# ⚠️ Disclaimer

This tool is for **educational and security research purposes only**.
Always ensure you have permission before crawling any website.

---

# ⚠️ Change the contact email in the script

The crawler currently sets a User-Agent with an email address. Please change that email to one you control (or remove it) so site operators can contact you if needed.

Locate this line in crawler.py:

session.headers.update({"User-Agent": "Crawler/1.0 (+Ghostting@bugcrowdninja.com)"})


Replace it with your own contact, for example:

session.headers.update({"User-Agent": "Crawler/1.0 (+yourname@yourdomain.com)"})


Or remove the email entirely if you prefer:

session.headers.update({"User-Agent": "Crawler/1.0"})

# 🧑‍💻 Author

**Ghostting** — [bugcrowdninja.com](https://bugcrowdninja.com)
Custom crawler for ethical reconnaissance.

---

Would you like me to include a **section for building a standalone executable (via PyInstaller)** or a **Docker usage section**? I can extend the README accordingly.
