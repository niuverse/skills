from __future__ import annotations

import logging
import threading
import time
from abc import ABC, abstractmethod
from datetime import date

import requests

from models import Comment, Post


logger = logging.getLogger("folds.scrapers")


class BaseScraper(ABC):
    def __init__(self, name: str, rate_limit_seconds: float = 1.0, timeout_seconds: float = 12.0) -> None:
        self.name = name
        self.rate_limit_seconds = rate_limit_seconds
        self.timeout_seconds = timeout_seconds
        self.session = requests.Session()
        self._last_request_at = 0.0
        self._throttle_lock = threading.Lock()

    @abstractmethod
    def search(
        self,
        topic: str,
        start_date: date | None,
        end_date: date | None,
        *,
        keywords: list[str] | None = None,
        limit: int | None = None,
    ) -> list[Post]:
        raise NotImplementedError

    @abstractmethod
    def get_comments(self, post_id: str, *, limit: int = 50) -> list[Comment]:
        raise NotImplementedError

    def close(self) -> None:
        self.session.close()

    def _throttle(self) -> None:
        if self.rate_limit_seconds <= 0:
            return
        with self._throttle_lock:
            elapsed = time.monotonic() - self._last_request_at
            if elapsed < self.rate_limit_seconds:
                time.sleep(self.rate_limit_seconds - elapsed)
            self._last_request_at = time.monotonic()

    def _get(self, url: str, *, params: dict[str, object] | None = None, headers: dict[str, str] | None = None) -> requests.Response:
        self._throttle()
        response = self.session.get(
            url,
            params=params,
            headers=headers,
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        return response
