from crawler.src.core.config import logger


async def wait_func(page):
    logger.info('INFINITE WAITING ENABLED!')
    while True:
        await page.wait_for_timeout(29000)
