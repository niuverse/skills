from __future__ import annotations

import logging
import re
from datetime import date, datetime

import requests
from bs4 import BeautifulSoup

from models import Comment, Post, slugify_topic_id
from scrapers.base import BaseScraper


logger = logging.getLogger("folds.scrapers.zhibo8")


class Zhibo8Scraper(BaseScraper):
    """直播吧爬虫 - 从热门新闻API提取数据"""

    DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15",
        "Accept": "application/json, text/html",
    }

    HOT_NEWS_URL = "https://m.zhibo8.cc/json/hot/24hours.htm"

    def __init__(self) -> None:
        super().__init__(name="zhibo8", rate_limit_seconds=1.0, timeout_seconds=15)

    def search(
        self,
        topic: str,
        start_date: date | None,
        end_date: date | None,
        *,
        keywords: list[str] | None = None,
        limit: int | None = None,
    ) -> list[Post]:
        """获取直播吧新闻（从热门列表中筛选）"""
        query_terms = [topic] + (keywords or [])
        target_limit = limit or 30
        all_posts: list[Post] = []

        # Fetch hot news
        try:
            response = self._get(
                self.HOT_NEWS_URL,
                headers=self.DEFAULT_HEADERS,
            )
            data = response.json()
            news_list = data.get("news", [])
            logger.info("Fetched %s hot news from zhibo8", len(news_list))
        except Exception as exc:
            logger.warning("Failed to fetch zhibo8 hot news: %s", exc)
            return []

        # Filter by keywords and date
        for item in news_list:
            title = item.get("title", "")
            if not title:
                continue

            # Check if matches any keyword
            if not self._matches_keywords(title, query_terms):
                continue

            # Parse time
            time_str = item.get("updatetime", "")
            post_time = self._parse_time(time_str)

            # Date filtering
            if start_date and post_time.date() < start_date:
                continue
            if end_date and post_time.date() > end_date:
                continue

            # Build URL
            url_path = item.get("url", "")
            if url_path.startswith("http"):
                url = url_path
            else:
                url = f"https://m.zhibo8.cc{url_path}"

            # Extract ID from URL
            post_id = self._extract_id(url_path) or str(hash(title) % 10000000)

            post = Post(
                id=post_id,
                topic_id=slugify_topic_id(topic),
                topic_name=topic,
                player=topic,
                source="zhibo8",
                source_url=url,
                posted_at=post_time,
                title=title[:200],
                content=title[:500],
                author="直播吧",
                likes=0,
                replies=0,
                event_tag=item.get("type", ""),
            )
            all_posts.append(post)

            if len(all_posts) >= target_limit:
                break

        logger.info(
            "Zhibo8 scraper fetched %s posts for topic='%s'",
            len(all_posts),
            topic,
        )
        return all_posts

    def _matches_keywords(self, text: str, keywords: list[str]) -> bool:
        """检查文本是否匹配关键词"""
        text_lower = text.lower()
        return any(kw.lower() in text_lower for kw in keywords if kw)

    def _parse_time(self, time_str: str) -> datetime:
        """解析时间字符串"""
        if not time_str:
            return datetime.now()

        time_str = time_str.strip()
        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y-%m-%d",
        ]

        for fmt in formats:
            try:
                return datetime.strptime(time_str, fmt)
            except ValueError:
                continue

        return datetime.now()

    def _extract_id(self, url_path: str) -> str | None:
        """从URL路径提取ID"""
        match = re.search(r"/(\d{4}-\d{2}-\d{2})/(\w+)\.htm", url_path)
        if match:
            return match.group(2)
        return None

    def get_comments(self, post_id: str, *, limit: int = 50) -> list[Comment]:
        """直播吧评论需要单独爬取页面"""
        logger.debug("Zhibo8 comments require page crawling. post_id=%s", post_id)
        return []
