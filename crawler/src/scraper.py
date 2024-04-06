import re

from playwright.async_api import BrowserContext

from crawler.src.core.config import settings, logger


async def scrape_video_links(browser: BrowserContext, channel_link: str) -> set[str]:
    """
    Скрапит все уникальные ссылки на видео на странице канала.
    :param browser: Объект браузера.
    :param channel_link: Ссылка на канал.
    :return: set() со всеми уникальными ссылками на странице канала.
    """
    page = await browser.new_page()
    await page.goto(channel_link, wait_until='load')
    await page.wait_for_timeout(settings.browser.PAGE_ADDITIONAL_LOADING_TIME_MS)

    link_locator = page.locator('css=a[href^="/watch?v="]')
    dirty_links: list[str] = await link_locator.evaluate_all("list => list.map(element => element.href)")

    url_pattern = re.compile("https://www\.youtube\.com/watch\?v=[A-z0-9-_]{11}")  # Паттерн url на видео  # noqa
    clean_links = {*filter(lambda link: re.fullmatch(url_pattern, link), dirty_links)}

    logger.info('Links found: %s.' % len(clean_links))
    await page.close()

    return clean_links
