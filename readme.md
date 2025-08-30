-----

## Scrapy 爬蟲專案 README.md

### 專案簡介

這是一個使用 Python 和 Scrapy 框架編寫的網路爬蟲，專為抓取 **koc.com.tw** 網站上的文章內容而設計。此爬蟲的核心功能是模擬網站的無限滾動（Infinite Scroll）行為，透過發送連續的 **AJAX POST 請求**來獲取所有頁面上的文章資料。


-----

### 檔案結構

本專案包含以下主要檔案：

  - `koc_crawler/spiders/koc.py`: 爬蟲的主要程式碼，定義了抓取邏輯。
  - `koc_crawler/items.py`: 定義了文章資料的結構 (`ArticleItem`)。
  - `koc_crawler/settings.py`: 專案的設定檔。

-----

### 如何執行

請確認您已安裝 Scrapy。您可以使用以下指令來執行爬蟲，並將抓取到的資料輸出為 JSON 或 CSV 檔案：

**輸出為 JSON 格式：**

```
scrapy crawl koc -o articles.json
```

**輸出為 CSV 格式：**

```
scrapy crawl koc -o articles.csv
```

-----

### 設定與客製化

您可以透過修改 `koc.py` 檔案中的 `MAX_PAGES` 變數來控制爬蟲要抓取多少頁。
例如，若要限制只抓取 5 頁，請將 `MAX_PAGES` 設為 `5`：

```python
class KocSpider(scrapy.Spider):
    ...
    MAX_PAGES = 5  # 設定您想要抓取的最大頁數
    ...
```

若您希望抓取所有頁面，可以將 `MAX_PAGES` 設定為一個足夠大的數字，或直接移除這個頁數限制的條件判斷。

-----

### 技術細節

此爬蟲的運作方式並非傳統的跟隨超連結。它模擬了網站的無限滾動機制，透過向網站的 AJAX API (`https://www.koc.com.tw/?ajax-request=jnews`) 發送 POST 請求來獲取內容。

每次請求都會在 `body` 中帶上 `data[current_page]` 參數，並在每次成功抓取後自動遞增，以實現頁面的連續抓取。伺服器回傳的是包含 HTML 內容的 JSON 資料，爬蟲會解析這些資料來提取所需的文章資訊。



---
# 🟢 完整流程（無分岔）

## 1. 建立 Scrapy 專案

在 VSCode 終端機（已啟用虛擬環境）輸入：

```powershell
scrapy startproject koc_crawler .
```

專案結構會長這樣：

```
koc_crawler/
    spiders/
        __init__.py
scrapy.cfg
```

---

## 2. 定義資料結構

打開 `koc_crawler/items.py`，改成：

```python
import scrapy

class ArticleItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    published_at = scrapy.Field()
    content = scrapy.Field()
```

---

## 3. 修改設定

打開 `koc_crawler/settings.py`，直接加上或修改這幾行：

```python
ROBOTSTXT_OBEY = False
FEED_EXPORT_ENCODING = "utf-8"

FEEDS = {
    "data/koc.jsonl": {"format": "jsonlines"},
}

DEFAULT_REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

DOWNLOAD_DELAY = 0.5
DEPTH_LIMIT = 2
LOG_LEVEL = "INFO"
```

---

## 4. 建立 Spider

新增檔案 `koc_crawler/spiders/blog_spider.py`，內容完整如下：

```python
import scrapy
from urllib.parse import urljoin
from koc_crawler.items import ArticleItem

class BlogSpider(scrapy.Spider):
    name = "koc"
    allowed_domains = ["koc.com.tw", "www.koc.com.tw"]
    start_urls = ["https://www.koc.com.tw/"]

    def parse(self, response):
        # 找文章連結（此為範例，實際上可依網站結構調整）
        article_links = response.css("a::attr(href)").getall()
        for href in article_links:
            url = urljoin(response.url, href)
            if any(domain in url for domain in self.allowed_domains):
                yield scrapy.Request(url, callback=self.parse_article)

    def parse_article(self, response):
        item = ArticleItem()
        item["url"] = response.url
        item["title"] = response.css("title::text").get(default="").strip()
        item["author"] = response.css(".author::text, .post-author::text").get(default="").strip()
        item["published_at"] = response.css("time::attr(datetime), .date::text").get(default="").strip()
        paragraphs = response.css("p::text").getall()
        item["content"] = "\n".join([p.strip() for p in paragraphs if p.strip()])
        yield item
```

---

## 5. 執行爬蟲

在專案根目錄（有 `scrapy.cfg` 的地方）執行：

```powershell
scrapy crawl koc
```

執行後，結果會存到：

```
data/koc.jsonl
```

你可以用 VSCode 或記事本打開來看，內容是一行一篇文章的 JSON。

---

