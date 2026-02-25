from __future__ import annotations

import logging
import re
from datetime import date, datetime

from models import Comment, Post, slugify_topic_id
from scrapers.base import BaseScraper


logger = logging.getLogger("folds.scrapers.dongqiudi")


class DongqiudiScraper(BaseScraper):
    """懂球帝爬虫 - 使用搜索API"""

    DEFAULT_HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }

    SEARCH_URL = "https://api.dongqiudi.com/search"

    def __init__(self) -> None:
        super().__init__(name="dongqiudi", rate_limit_seconds=1.0, timeout_seconds=15)

    def search(
        self,
        topic: str,
        start_date: date | None,
        end_date: date | None,
        *,
        keywords: list[str] | None = None,
        limit: int | None = None,
    ) -> list[Post]:
        """搜索懂球帝新闻"""
        query_terms = [topic] + (keywords or [])
        target_limit = limit or 30
        all_posts: list[Post] = []

        # Search with different query terms
        for query in query_terms[:3]:
            if len(all_posts) >= target_limit:
                break

            for page in range(1, 4):
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

        # Remove duplicates
        seen_ids: set[str] = set()
        unique_posts: list[Post] = []
        for post in all_posts:
            if post.id not in seen_ids:
                seen_ids.add(post.id)
                unique_posts.append(post)
                if len(unique_posts) >= target_limit:
                    break

        logger.info(
            "Dongqiudi scraper fetched %s unique posts for topic='%s'",
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
        params = {
            "keywords": query,
            "type": "all",
            "page": page,
        }

        try:
            response = self._get(
                self.SEARCH_URL,
                params=params,
                headers=self.DEFAULT_HEADERS,
            )
            data = response.json()
        except Exception as exc:
            logger.debug("Dongqiudi search failed: %s", exc)
            return []

        posts: list[Post] = []

        # Process news items
        news_items = data.get("news", [])
        for item in news_items:
            title = self._clean_html(item.get("title", ""))
            if not title:
                continue

            article_id = str(item.get("id", ""))
            if not article_id:
                continue

            # Build URL
            url = f"https://www.dongqiudi.com/article/{article_id}"

            # Parse time (API doesn't always return time)
            post_time = datetime.now()

            # Date filtering (limited since API doesn't return consistent time)
            if start_date and end_date:
                # Skip filtering if we don't have reliable time data
                pass

            post = Post(
                id=article_id,
                topic_id=slugify_topic_id(topic),
                topic_name=topic,
                player=topic,
                source="dongqiudi",
                source_url=url,
                posted_at=post_time,
                title=title[:200],
                content=title[:500],
                author="懂球帝",
                likes=item.get("up_count", 0) or 0,
                replies=item.get("comment_count", 0) or 0,
                event_tag="",
            )
            posts.append(post)

        # Also process topics if available
        topic_items = data.get("topics", [])
        for item in topic_items:
            title = self._clean_html(item.get("title", ""))
            if not title:
                continue

            topic_id = str(item.get("id", ""))
            if not topic_id or topic_id in [p.id for p in posts]:
                continue

            url = f"https://www.dongqiudi.com/topic/{topic_id}"

            post = Post(
                id=f"topic_{topic_id}",
                topic_id=slugify_topic_id(topic),
                topic_name=topic,
                player=topic,
                source="dongqiudi",
                source_url=url,
                posted_at=datetime.now(),
                title=title[:200],
                content=title[:500],
                author="懂球帝",
                likes=0,
                replies=item.get("post_count", 0) or 0,
                event_tag="topic",
            )
            posts.append(post)

        return posts

    def _clean_html(self, text: str) -> str:
        """清理HTML标签"""
        if not text:
            return ""
        # Remove font tags and other HTML
        text = re.sub(r"<font[^>]*>", "", text)
        text = re.sub(r"</font>", "", text)
        text = re.sub(r"<[^>]+>", "", text)
        return text.strip()

    def get_comments(self, post_id: str, *, limit: int = 50) -> list[Comment]:
        """获取懂球帝文章评论"""
        # Remove topic_ prefix if present
        clean_id = post_id.replace("topic_", "")
        url = f"https://api.dongqiudi.com/v2/article/{clean_id}/comment"

        try:
            response = self._get(url, headers=self.DEFAULT_HEADERS)
            data = response.json()
            result = data.get("data", {})
            comments_data = result.get("comment_list", [])

            comments: list[Comment] = []
            for c in comments_data[:limit]:
                content = c.get("content", "")
                author = c.get("user_name", "匿名")
                likes = c.get("up_num", 0)
                time_str = c.get("created_at", "")

                # Parse time
                try:
                    posted_at = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
                except:
                    posted_at = datetime.now()

                comments.append(
                    Comment(
                        id=str(c.get("id", hash(content) % 10000000)),
                        content=content,
                        author=author,
                        posted_at=posted_at,
                        likes=likes,
                    )
                )

            logger.info("Fetched %s comments for article %s", len(comments), clean_id)
            return comments
        except Exception as exc:
            logger.warning("Failed to fetch comments for %s: %s", post_id, exc)
            return []
