import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "https://www.shl.com"
CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
}

# ---------- session with retry ----------
def get_session():
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=1.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update(HEADERS)
    return session


def get_description(session, url):
    try:
        r = session.get(url, timeout=60)
        soup = BeautifulSoup(r.text, "html.parser")
        return soup.get_text(" ", strip=True)[:3000]
    except Exception as e:
        print("Detail page failed:", url)
        return ""


def find_individual_table(soup):
    for table in soup.find_all("table"):
        th = table.find("th")
        if th and "Individual Test Solutions" in th.get_text():
            return table
    return None


def crawl():
    session = get_session()
    all_rows = []
    start = 0

    while True:
        page_url = f"{CATALOG_URL}?start={start}&type=1"
        print(f"\nFetching: {page_url}")

        try:
            r = session.get(page_url, timeout=60)
        except Exception as e:
            print("Catalog page failed, retrying after delay...")
            time.sleep(5)
            continue

        soup = BeautifulSoup(r.text, "html.parser")
        table = find_individual_table(soup)

        if table is None:
            print("No Individual Test Solutions table found. Stopping.")
            break

        rows = table.find_all("tr", attrs={"data-entity-id": True})
        print("Rows found:", len(rows))

        if not rows:
            break

        for row in tqdm(rows, desc=f"Page {start//12 + 1}"):
            a = row.select_one("td.custom__table-heading__title a")
            if not a:
                continue

            name = a.get_text(strip=True)
            url = BASE_URL + a["href"]

            tds = row.find_all("td")
            remote = "Yes" if tds[1].select_one(".-yes") else "No"
            adaptive = "Yes" if tds[2].select_one(".-yes") else "No"

            test_types = [
                span.get_text(strip=True)
                for span in row.select("span.product-catalogue__key")
            ]

            description = get_description(session, url)

            all_rows.append({
                "name": name,
                "url": url,
                "remote_support": remote,
                "adaptive_support": adaptive,
                "test_type": ",".join(test_types),
                "description": description
            })

            time.sleep(0.7)  # polite crawling

        start += 12
        time.sleep(2)  # pause between pages

    df = pd.DataFrame(all_rows)
    df.to_csv("data/raw/shl_catalog.csv", index=False)

    print("\nCrawl completed.")
    print("Total assessments:", len(df))


if __name__ == "__main__":
    crawl()
