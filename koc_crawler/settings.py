# Scrapy settings for koc_crawler project

BOT_NAME = "koc_crawler"

SPIDER_MODULES = ["koc_crawler.spiders"]
NEWSPIDER_MODULE = "koc_crawler.spiders"

# --- 爬蟲設定 ---
ROBOTSTXT_OBEY = False          # 改成 False，不受 robots.txt 限制
CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 0.5            # 放慢一點，避免伺服器封鎖

# --- 輸出編碼與檔案設定 ---
FEED_EXPORT_ENCODING = "utf-8"
FEEDS = {
    "data/koc.jsonl": {"format": "jsonlines"},
}

# --- 請求標頭（避免被擋掉） ---
DEFAULT_REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

# --- 日誌 ---
LOG_LEVEL = "INFO"

# --- 其餘保持預設即可 ---
# ITEM_PIPELINES = {
#     "koc_crawler.pipelines.KocCrawlerPipeline": 300,
# }
