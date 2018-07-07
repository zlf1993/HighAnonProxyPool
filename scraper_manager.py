import re
import urllib.request
import lxml.html

IntervalDelay = 20


def download(url, headers=None, proxy=None, num_retries=4):
    print('Downloading:', url)
    opener = urllib.request.build_opener()
    if headers:
        urllib.request.Request(url, headers)
    if proxy:
        proxy_params = {urllib.parse.urlparse(url).scheme: proxy}
        opener.add_handler(urllib.request.ProxyHandler(proxy_params))
    try:
        urllib.request.install_opener(opener)
        response = urllib.request.urlopen(url)
        html = response.read().decode('utf-8')
    except urllib.error.URLError as e:
        print("Download error", e.reason)
        # URLError has reason
        print("Code:", e.code)
        # HTTPError has reason, code, HTTPError is subclass of URLError
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # retry 5XX HTTP errors
                return download(url, headers, proxy, num_retries - 1)
    return html


def proxy_list_org():
    Re_Pattern_IP = re.compile("(.*):")
    Re_Pattern_PORT = re.compile(":(.*)")
    BASE_URL = "https://proxy-list.org/english/index.php?p="
    # print("[!] Scraping proxy-list.org...")
    for startingURL_Param in range(1, 2):
        url = BASE_URL + str(startingURL_Param)
        html = download(url)
        if html:
            tree = lxml.html.fromstring(html)
            fixed_html = lxml.html.tostring(tree,pretty_print=True)
            print(fixed_html)


if __name__ == "__main__":
    proxy_list_org()
