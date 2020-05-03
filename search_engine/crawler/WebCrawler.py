from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse
from crawler.utils import *

'''
Web Crawler to crawl data starting from base url
'''


class WebCrawler:

    def __init__(self, base_url):

        self.base_url = base_url
        self.root_url = '{}://{}'.format(urlparse(self.base_url).scheme, urlparse(self.base_url).netloc)
        self.pool = ThreadPoolExecutor(max_workers=10)
        self.domain = 'uic.edu'
        self.invalid_extensions = ["pdf", "jpg", "jpeg", "doc", "docx", "ppt", "pptx", "png", "txt", "exe", "ps", "psb",
                                   "aspx"]
        # Already crawled links
        self.crawled_links = set([])
        # Initalising queue
        # Initalising queue
        self.queue = Queue()

        # Adding base url to the queue
        self.queue.put(self.base_url)

    def is_valid_extension(self, url):
        extension = url.split('.')[-1]
        if extension in self.invalid_extensions:
            return False
        return True

    def parse_links(self, html, node_link):
        links = scrape_links(html)
        for link in links:
            url = link['href']
            if (url.startswith('/') or self.domain in url) and ('.com' not in url):  # run only in the uic.edu domain
                url = urljoin(self.root_url, url)
                # url = re.search('.+?uic.edu', url).group(0)
                if url not in self.crawled_links and '@' not in url and self.is_valid_extension(url):
                    if not url.endswith("/"):
                        url = url + "/"  # appending / in the end to avoid duplicate runs
                    if "https" not in url:
                        url = url.replace("http", "https")
                    self.queue.put(url)

    def post_scrape_callback(self, res):
        result = res.result()
        if result is not None:
            # result = res
            if result[0] and result[
                0].status_code == 200:  # only if the http request was successful get the text and other links
                self.parse_links(result[0].text, result[1])
                scrape_info(result[0].text, result[1])

    def run_scraper(self):
        while True:
            try:
                target_url = self.queue.get(timeout=120)  # wait for 60 sec for a page to add a url to be parsed
                if target_url not in self.crawled_links:  # Avoiding cycles ->if page is
                    # already scraped then donot continue
                    print(" Scraping URL: {}".format(target_url))
                    self.crawled_links.add(target_url)
                    job = self.pool.submit(scrape_link, target_url)
                    job.add_done_callback(self.post_scrape_callback)
            except Empty:
                return
            except Exception as e:
                print(e)
                continue
