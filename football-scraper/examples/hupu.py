from __future__ import annotations

import logging
import re
from datetime import date, datetime
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from models import Comment, Post, slugify_topic_id
from scrapers.base import BaseScraper


logger = logging.getLogger("folds.scrapers.hupu")


class HupuScraper(BaseScraper):
    """虎扑爬虫 - 从搜索结果直接提取数据"""

    DEFAULT_HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }

    def __init__(self) -> None:
        super().__init__(name="hupu", rate_limit_seconds=1.0, timeout_seconds=15)

    def search(
        self,
        topic: str,
        start_date: date | None,
        end_date: date | None,
        *,
        keywords: list[str] | None = None,
        limit: int | None = None,
    ) -> list[Post]:
        """搜索虎扑帖子"""
        query_terms = self._build_query_terms(topic, keywords)
        target_limit = limit or 50
        all_posts: list[Post] = []

        # Search with different query terms
        for query in query_terms[:3]:  # Limit to first 3 terms
            if len(all_posts) >= target_limit:
                break

            for page in range(1, 4):  # Max 3 pages
                posts = self._search_page(
                    query=query,
                    page=page,
                    topic=topic,
                    start_date=start_date,
                    end_date=end_date,
                )
                all_posts.extend(posts)

                if len(all_posts) >= target_limit:
                    break

        # Remove duplicates by URL
        seen_urls: set[str] = set()
        unique_posts: list[Post] = []
        for post in all_posts:
            if post.source_url and post.source_url not in seen_urls:
                seen_urls.add(post.source_url)
                unique_posts.append(post)
                if len(unique_posts) >= target_limit:
                    break

        logger.info(
            "Hupu scraper fetched %s unique posts for topic='%s'",
            len(unique_posts),
            topic,
        )
        return unique_posts

    def _search_page(
        self,
        query: str,
        page: int,
        topic: str,
        start_date: date | None,
        end_date: date | None,
    ) -> list[Post]:
        """搜索单个页面"""
        search_url = "https://bbs.hupu.com/search"
        params = {"q": query, "page": page}

        try:
            response = self._get(search_url, params=params, headers=self.DEFAULT_HEADERS)
        except Exception as exc:
            logger.debug("Search request failed: %s", exc)
            return []

        return self._parse_search_results(
            html=response.text,
            topic=topic,
            start_date=start_date,
            end_date=end_date,
        )

    def _parse_search_results(
        self,
        html: str,
        topic: str,
        start_date: date | None,
        end_date: date | None,
    ) -> list[Post]:
        """解析搜索结果页面"""
        soup = BeautifulSoup(html, "html.parser")
        posts: list[Post] = []

        # Find all thread links
        thread_links = soup.find_all("a", href=re.compile(r"/\d+\.html$"))

        for link in thread_links:
            href = link.get("href", "")
            title = link.get_text(strip=True)

            if not title or len(title) < 5:
                continue

            # Skip navigation links
            if any(x in href for x in ["/bxj", "forum", "board"]):
                continue

            # Build full URL
            if href.startswith("/"):
                url = f"https://bbs.hupu.com{href}"
            elif href.startswith("http"):
                url = href
            else:
                continue

            # Extract post ID
            post_id_match = re.search(r"/(\d+)\.html", href)
            post_id = post_id_match.group(1) if post_id_match else "0"

            # Find parent element for additional info
            parent = link.find_parent(["li", "div", "tr", "article"])
            author = "匿名用户"
            post_time = None
            likes = 0
            replies = 0

            if parent:
                # Try to find author
                author_elem = parent.find(
                    ["a", "span"],
                    class_=re.compile(r"author|user|name|author-name"),
                )
                if author_elem:
                    author = author_elem.get_text(strip=True)[:20] or "匿名用户"

                # Try to find time
                time_elem = parent.find("time")
                if time_elem:
                    time_str = time_elem.get("datetime") or time_elem.get_text(strip=True)
                    post_time = self._parse_time(time_str)
                else:
                    # Try to find time in text
                    time_match = re.search(
                        r"(\d{4}-\d{2}-\d{2}|\d{2}-\d{2}\s+\d{2}:\d{2})",
                        parent.get_text(),
                    )
                    if time_match:
                        post_time = self._parse_time(time_match.group(1))

                # Try to find likes/replies count
                text = parent.get_text()
                likes_match = re.search(r"(\d+)\s*亮", text)
                if likes_match:
                    likes = int(likes_match.group(1))
                replies_match = re.search(r"(\d+)\s*回复", text)
                if replies_match:
                    replies = int(replies_match.group(1))

            # Default time if not found
            if post_time is None:
                post_time = datetime.now()

            # Date filtering
            if start_date and post_time.date() < start_date:
                continue
            if end_date and post_time.date() > end_date:
                continue

            post = Post(
                id=post_id,
                topic_id=slugify_topic_id(topic),
                topic_name=topic,
                player=topic,
                source="hupu",
                source_url=url,
                posted_at=post_time,
                title=title[:200],
                content=title[:500],  # Use title as content initially
                author=author,
                likes=likes,
                replies=replies,
                event_tag="",
            )
            posts.append(post)

        return posts

    def _build_query_terms(self, topic: str, keywords: list[str] | None) -> list[str]:
        """构建搜索词列表"""
        terms = [topic]
        if keywords:
            terms.extend(keywords)
        # Remove duplicates while preserving order
        seen: set[str] = set()
        result: list[str] = []
        for term in terms:
            normalized = term.strip()
            lowered = normalized.lower()
            if normalized and lowered not in seen:
                seen.add(lowered)
                result.append(normalized)
        return result

    def _parse_time(self, time_str: str) -> datetime:
        """解析时间字符串"""
        if not time_str:
            return datetime.now()

        time_str = time_str.strip()

        # Try different formats
        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y-%m-%d",
            "%m-%d %H:%M",
            "%H:%M",
        ]

        for fmt in formats:
            try:
                dt = datetime.strptime(time_str, fmt)
                # Handle year-less formats
                if fmt in ("%m-%d %H:%M", "%H:%M"):
                    dt = dt.replace(year=datetime.now().year)
                    # If resulting date is in future, assume last year
                    if dt > datetime.now():
                        dt = dt.replace(year=dt.year - 1)
                return dt
            except ValueError:
                continue

        # Fallback to now
        return datetime.now()

    def get_comments(self, post_id: str, *, limit: int = 50) -> list[Comment]:
        """
        获取评论 - 虎扑详情页是动态加载的，此方法暂返回空列表
        如需完整评论，需要使用浏览器自动化（playwright/selenium）
        """
        logger.debug(
            "Comments fetching requires browser automation for post_id=%s", post_id
        )
        return []
