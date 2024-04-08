from playwright.async_api import Page

from crawler.src.core.config import logger


async def _format_video_selector() -> str:
    """Форматирует селектор для получения коротких ссылок на видео.

    preview_selector - Селектор для элемента-ссылки на preview.
    content_selector - Селектор для элемента-ссылки на ролики из списков на главной.
    """
    preview_selector = 'a.ytp-title-link[href]'
    content_selector = 'a#video-title'

    result_selector = f'css={preview_selector},{content_selector}'
    return result_selector


async def _scrape_video_ids(page) -> list[str]:
    """Скрапит список video_id.

    Получает короткие ссылки с помощью селектора.
    Каждая обрезается до ID через JS.
    """
    selector = await _format_video_selector()
    locator = page.locator(selector)

    video_ids = await locator.evaluate_all("list => list.map(element => element.search.slice(3, 14))")
    unique_video_ids = list(set(video_ids))

    return unique_video_ids


async def scrape_video_ids(page: Page, channel_link: str) -> list[str]:
    """
    Скрапит ID всех видео.

    :param page: Объект страницы.
    :param channel_link: Ссылка на канал.
    :return: ID всех видео на Главной странице канала.
    """

    video_ids = await _scrape_video_ids(page)
    logger.info('По каналу %s получено %s ID.' % (channel_link, len(video_ids)))

    return video_ids
