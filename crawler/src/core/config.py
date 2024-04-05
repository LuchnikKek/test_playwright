import logging

HEADLESS = False
MAX_PAGES = 3
PAGE_ADDITIONAL_LOADING_TIME_MS = 5000
VIEWPORT_WIDTH = 1920
VIEWPORT_HEIGHT = 1080
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
USERAGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.4 Safari/537.36"
LOG_FORMAT = "%(levelname)s - %(asctime)s - %(message)s"
LOG_LEVEL = "INFO"

logger = logging.getLogger('crawler')
logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)
