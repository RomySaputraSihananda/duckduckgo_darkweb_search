import pytest
from typing import Callable
from loguru import logger

from concurrent.futures import ThreadPoolExecutor, Future
from duckduckgo_search import DDGS

@pytest.fixture
def ddgs() -> DDGS:
    return DDGS(
        proxies={
            'http': 'socks5h://192.168.29.65:32090',
            'https': 'socks5h://192.168.29.65:32090'
        }
    )

def test_text(
    ddgs: DDGS,
    count: int
) -> list[dict[str, str]]:
    try:
        data: list[dict[str,str]] = ddgs.text(
            "cat", 
            safesearch="off", 
            timelimit="m", 
            max_results=30
        )
        logger.info(
        'requests ke -> %d len -> %d' % (count, len(data))
        )
        return data
    except BaseException as e:
        logger.error(e)
        return

def test_text_html(
    ddgs: DDGS,
    count: int
) -> list[dict[str, str]]:
    try:
        data: list[dict[str,str]] = ddgs.text(
            "eagle", 
            backend="html", 
            max_results=30
        )
        logger.info(
        'requests ke -> %d len -> %d' % (count, len(data))
        )
        return data
    except BaseException as e:
        logger.error(e)
        return

def test_text_lite(
    ddgs: DDGS,
    count: int
) -> list[dict[str, str]]:
    try:
        data: list[dict[str,str]] = ddgs.text(
            "dog", 
            backend="lite", 
            max_results=30
        )
        logger.info(
        'requests ke -> %d len -> %d' % (count, len(data))
        )
        return data
    except BaseException as e:
        logger.error(e)
        return


def test_images(
    ddgs: DDGS,
    count: int
) -> list[dict[str, str]]:
    try:
        data: list[dict[str,str]] = ddgs.images(
            "flower", 
            max_results=200
        )
        logger.info(
        'requests ke -> %d len -> %d' % (count, len(data))
        )
        return data
    except BaseException as e:
        logger.error(e)
        return

def test_videos(
    ddgs: DDGS,
    count: int
) -> list[dict[str, str]]:
    try:
        data: list[dict[str,str]] = ddgs.videos(
            "sea", max_results=40
        )
        logger.info(
        'requests ke -> %d len -> %d' % (count, len(data))
        )
        return data
    except BaseException as e:
        logger.error(e)
        return

def test_news(
    ddgs: DDGS,
    count: int
) -> list[dict[str, str]]:
    try:
        data: list[dict[str,str]] = ddgs.news(
            "tesla", 
            max_results=30
        )
        logger.info(
        'requests ke -> %d len -> %d' % (count, len(data))
        )
        return data
    except BaseException as e:
        logger.error(e)
        return

def test_limit(
    ddgs: DDGS,
    target: Callable[[DDGS, int], list[dict[str,str]]]
) -> None:
    with ThreadPoolExecutor(
        max_workers=10
    ) as w:
        futures: list[Future] = []
        count: int = 1
        # while(True):
        for _ in range(10):
            futures.append(
                w.submit(
                    target,        
                    ddgs,
                    count
                )
            )
            count += 1

    for future in futures:
        future.result()

    
def test_limit_func_text(
    ddgs: DDGS
) -> None:
    test_limit(
        ddgs,
        test_text
    )

def test_limit_func_text_html(
    ddgs: DDGS,
) -> None:
    test_limit(
        ddgs,
        test_text_html
    )

def test_limit_func_text_lite(
    ddgs: DDGS,
) -> None:
    test_limit(
        ddgs,
        test_text_lite
    )

def test_limit_func_images(
    ddgs: DDGS,
) -> None:
    test_limit(
        ddgs,
        test_images
    )

def test_limit_func_videos(
    ddgs: DDGS,
) -> None:
    test_limit(
        ddgs,
        test_videos
    )

def test_limit_func_news(
    ddgs: DDGS
) -> None:
    test_limit(
        ddgs,
        test_news
    )