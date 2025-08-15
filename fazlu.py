import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

base_url = "http://mis.dgfp.gov.bd/ss/"
menu_url = urljoin(base_url, "ss_menu.php")

try:
    response = requests.get(menu_url, timeout=10)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Failed to fetch menu page: {e}")
    exit()

soup = BeautifulSoup(response.text, "html.parser")
links = soup.find_all("a")

for link in links:
    href = link.get("href")
    if not href:
        continue
    href = href.strip()
    # Skip anchors, javascript pseudo-links and mailto links
    if href == "#" or href.startswith("javascript:") or href.startswith("mailto:"):
        continue

    full_url = urljoin(base_url, href)

    try:
        r = requests.get(full_url, timeout=5)
        # Only show links that are not OK (status code != 200)
        if r.status_code != 200:
            print(f"{full_url} → {r.status_code}")
    except requests.exceptions.RequestException:
        print(f"{full_url} → ERROR")
