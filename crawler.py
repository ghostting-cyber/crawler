import argparse
import requests
from bs4 import BeautifulSoup
from collections import deque
from urllib.parse import urljoin, urldefrag, urlparse
import time
import sys
from pyfiglet import Figlet
import tldextract

f = Figlet(font='larry3d')
print(f.renderText('crawler'))

def normalize_url(base, link):
    # resolve relative links e tira fragmentos da url
    try:
        joined = urljoin(base, link)
        nofrag, _ = urldefrag(joined)
        return nofrag
    except Exception:
        return link

def is_html(link):
    p = urlparse(link)
    return p.scheme in ("http", "https")

def crawl (start_url, delay=0.5, output_file=None):
    session = requests.Session()
    session.headers.update({"User-Agent": "Crawler/1.0 (+Ghostting@bugcrowdninja.com)"})

    print(f"[+] Started crawling for => {start_url}\n")

    to_visit = deque([start_url])
    visited = set()
    seen_output = set() # para evitar enviar o mesmo link no output
    enqueued = set([start_url])

    # extrai o domínio registrável da start_url
    start_domain_info = tldextract.extract(start_url)
    start_reg_domain = start_domain_info.registered_domain

    # abrir o arquivo de output (caso tenha sido requisitado)
    out_f = None
    if output_file:
        out_f = open(output_file, "w", encoding="utf-8")
    
    try:
        while to_visit:
            current = to_visit.popleft()
            if current in visited:
                continue
            visited.add(current)

            # print the current url as a discovered link if not printed before
            if current not in seen_output:
                print(current)
                seen_output.add(current)
                if out_f:
                    out_f.write(current + "\n")
                    out_f.flush()

            # Only attempt HTTP(S) fetches
            if not is_html(current):
                # non-http links are printed above, but not fetched
                continue

            try:
                resp = session.get(current, timeout=10, allow_redirects=True)
            except requests.exceptions.RequestException:
                time.sleep(delay)
                continue

            content_type = resp.headers.get("Content-Type", "")
            if "html" not in content_type.lower():
                time.sleep(delay)
                continue
            
            # Parse HTML and extract all <a href>
            try:
                soup = BeautifulSoup(resp.text, "html.parser")
            except Exception:
                time.sleep(delay)
                continue

            # Find all anchors and normalize them, print each (and enqueue http(s) ones)
            for a in soup.find_all("a"):
                href = a.get("href")
                if href is None:
                    continue
                norm = normalize_url(resp.url, href)

                # filtra para o mesmo domínio registrável (aceita subdomínios)
                norm_domain_info = tldextract.extract(norm)
                norm_reg_domain = norm_domain_info.registered_domain
                if norm_reg_domain != start_reg_domain:
                    continue

                # print every link found (one per line), but avoid duplicates in output
                if norm not in seen_output:
                    print(norm)
                    seen_output.add(norm)
                    if out_f:
                        out_f.write(norm + "\n")
                        out_f.flush()
                
                # enqueue for crawling if HTTP(S) and not visited yet
                if is_html(norm) and norm not in visited and norm not in enqueued:
                    to_visit.append(norm)
                    enqueued.add(norm)

            time.sleep(delay)

    finally:
        if out_f:
            out_f.close()

def main():
    parser = argparse.ArgumentParser(description="Web Crawler - Extracts and prints all links from a starting URL.")
    parser.add_argument("-u", "--url", required=True, help="The starting URL to crawl.")
    parser.add_argument("-o", "--output", help="Optional output file to save discovered links.")
    parser.add_argument("-d", "--delay", type=float, default=0.5, help="Delay between requests in seconds (default: 0.5s).")
    args = parser.parse_args()

    try:
        crawl(args.url, delay=args.delay, output_file=args.output)
    except KeyboardInterrupt:
        print("\n[!] Crawler interrupted by user. Exiting...", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()