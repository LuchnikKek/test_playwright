from playwright.async_api import Page


async def scrape_video_ids(page: Page) -> list[str]:
    """Скрапит ID всех видео со страницы.

    Args:
        page: Объект страницы.
    Returns:
        video_ids: Список со всеми уникальными ID видео на странице. Только ID, без параметра "v=".
    """
    videos_locator = page.locator(_videos_selector())
    js_query = _videos_to_ids_js_query()
    video_ids = await videos_locator.evaluate_all(expression=js_query)

    unique_video_ids = list(set(video_ids))

    return unique_video_ids


def _videos_selector() -> str:
    """Возвращает селектор для получения всех видео.

    На странице канала есть списки со всеми роликами.
    Но тот, что проигрывается при открытии канала имеет другой селектор.
    Функция возвращает общий селектор для списков роликов + ролика при открытии канала.
    """
    video_playlists_selector = "ytd-item-section-renderer.style-scope a#video-title"
    video_preview_selector = "a.ytp-title-link[href]"
    return "css=%s,%s" % (video_preview_selector, video_playlists_selector)


def _videos_to_ids_js_query() -> str:
    """Возвращает JS-запрос для получения списка id видео из списка элементов.

    Поле .search для каждого элемента построено по принципу:
    '?v={video_id}[иногда дополнительные параметры]'
    Указанный запрос вырезает video_id для всех элементов.
    """
    return "list => list.map(element => element.search.slice(3, 14))"
