from contextlib import asynccontextmanager

from playwright.async_api import Playwright, BrowserContext, async_playwright, Route

from src.core.config import settings, logger


@asynccontextmanager
async def browser_context() -> BrowserContext:
    """Создаёт новый асинхронный контекстный менеджер браузера в зависимости от значений в конфиге."""
    async with async_playwright() as context:
        browser = await _headless_browser(context) if settings.browser.HEADLESS else await _headful_browser(context)

        # Автоматическое отклонение запросов на гугл-сервисы
        await browser.route("**/{play,accounts}.google.com/**", _abort_handler)

        try:
            logger.debug("Открыл браузер.")
            yield browser
        finally:
            await browser.close()
            logger.debug("Закрыл браузер.")


async def _headless_browser(playwright_context: Playwright) -> BrowserContext:
    """Возвращает Headless браузер.

    Аргумент --headless=new указывает использовать новый headless режим.
    Официально он не поддерживается Playwright, но в обычном вообще не видел страницу.
    """
    _browser = await playwright_context.chromium.launch(args=["--headless=new"], headless=False)
    browser = await _browser.new_context(user_agent=settings.browser.USERAGENT)
    return browser


async def _headful_browser(playwright_context: Playwright) -> BrowserContext:
    """Возвращает Headful браузер."""
    _browser = await playwright_context.chromium.launch(args=["--start-maximized"], headless=False)
    browser = await _browser.new_context(
        user_agent=settings.browser.USERAGENT,
        viewport={
            "width": settings.browser.VIEWPORT_WIDTH,
            "height": settings.browser.VIEWPORT_HEIGHT,
        },
        screen={
            "width": settings.browser.SCREEN_WIDTH,
            "height": settings.browser.SCREEN_HEIGHT,
        },
    )
    return browser


async def _abort_handler(route: Route):
    """Обработчик, отклоняющий запрос.

    REQUEST_ABORTION_CODE: код, с которым отклоняется запрос. Подробнее в доке:
    https://playwright.dev/python/docs/api/class-route#route-abort-option-error-code
    """
    logger.debug("Aborted request to %s." % route.request.url)
    await route.abort(settings.browser.REQUEST_ABORTION_CODE)
