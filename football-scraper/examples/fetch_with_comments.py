from __future__ import annotations

import asyncio
import json
import logging
import re
from datetime import date, datetime
from pathlib import Path

from models import Post, RawPostsFile, Topic, load_topics_config
from scrapers import get_scraper


logger = logging.getLogger("folds.fetch")


def _resolve_topic(topic: str | None, player: str | None) -> Topic:
    query = topic or player or "内马尔"
    config = load_topics_config()
    return config.require(query)


def _resolve_range(
    *,
    topic: Topic,
    start_date: date | None,
    end_date: date | None,
) -> tuple[date, date]:
    resolved_start = start_date or topic.time_range.start
    resolved_end = end_date or topic.time_range.end
    if resolved_start > resolved_end:
        raise ValueError("Resolved date range is invalid: start date is later than end date.")
    return resolved_start, resolved_end


def _post_dedupe_key(post: Post) -> str:
    if post.source_url:
        return f"url::{post.source}::{post.source_url.rstrip('/')}"
    normalized_title = re.sub(r"\s+", "", post.title).casefold()
    return f"title::{post.source}::{normalized_title}::{post.posted_at.date().isoformat()}"


def _dedupe_posts(posts: list[Post]) -> list[Post]:
    deduped: dict[str, Post] = {}
    for post in sorted(posts, key=lambda item: item.posted_at):
        key = _post_dedupe_key(post)
        deduped.setdefault(key, post)
    return list(deduped.values())


def _normalize_post(post: Post, topic: Topic) -> Post:
    return post.model_copy(
        update={
            "topic_id": topic.id,
            "topic_name": topic.name,
            "player": topic.name,
            "event_tag": post.event_tag or topic.category,
        }
    )


async def _fetch_platform(
    *,
    platform: str,
    topic: Topic,
    start_date: date,
    end_date: date,
    limit: int | None,
    fetch_comments: bool = True,
    comments_per_post: int = 10,
) -> list[Post]:
    scraper = get_scraper(platform)
    logger.info("Fetching topic='%s' from platform='%s'", topic.name, platform)
    try:
        posts = await asyncio.to_thread(
            scraper.search,
            topic.name,
            start_date,
            end_date,
            keywords=topic.keywords,
            limit=limit,
        )
        normalized = [_normalize_post(post, topic) for post in posts]
        
        # Fetch comments for each post
        if fetch_comments:
            for post in normalized:
                try:
                    comments = await asyncio.to_thread(
                        scraper.get_comments,
                        post.id,
                        limit=comments_per_post,
                    )
                    post.comments = comments
                    logger.debug(
                        "Fetched %s comments for post %s", len(comments), post.id
                    )
                except Exception as exc:
                    logger.debug("Failed to fetch comments for %s: %s", post.id, exc)
        
        return normalized
    finally:
        scraper.close()


async def _collect_posts(
    *,
    topic: Topic,
    start_date: date,
    end_date: date,
    limit: int | None,
) -> list[Post]:
    tasks = [
        _fetch_platform(
            platform=platform,
            topic=topic,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
        )
        for platform in topic.platforms
    ]

    if not tasks:
        return []

    results = await asyncio.gather(*tasks, return_exceptions=True)
    merged: list[Post] = []

    for platform, result in zip(topic.platforms, results):
        if isinstance(result, Exception):
            logger.exception("Platform fetch failed for %s", platform, exc_info=result)
            continue
        merged.extend(result)

    return merged


def run(
    *,
    player: str | None = None,
    topic: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    limit: int | None = None,
) -> Path:
    selected_topic = _resolve_topic(topic=topic, player=player)
    resolved_start, resolved_end = _resolve_range(
        topic=selected_topic,
        start_date=start_date,
        end_date=end_date,
    )

    logger.info(
        "Fetch stage started. topic=%s, platforms=%s, start_date=%s, end_date=%s, limit=%s",
        selected_topic.name,
        ",".join(selected_topic.platforms),
        resolved_start,
        resolved_end,
        limit,
    )

    posts = asyncio.run(
        _collect_posts(
            topic=selected_topic,
            start_date=resolved_start,
            end_date=resolved_end,
            limit=limit,
        )
    )
    posts = _dedupe_posts(posts)
    posts.sort(key=lambda item: item.posted_at)

    if limit is not None:
        posts = posts[:limit]

    if not posts:
        raise ValueError(
            "No posts fetched. Check topic/platform settings, network connectivity, or date range."
        )

    output_dir = Path("data") / selected_topic.name
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "raw_posts.json"

    payload = RawPostsFile(
        topic_id=selected_topic.id,
        topic_name=selected_topic.name,
        player=selected_topic.name,
        generated_at=datetime.now(),
        start_date=resolved_start,
        end_date=resolved_end,
        platforms=selected_topic.platforms,
        total_posts=len(posts),
        posts=posts,
    )
    output_path.write_text(
        json.dumps(payload.model_dump(mode="json"), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    logger.info(
        "Fetch stage completed. topic=%s, total_posts=%s, output=%s",
        selected_topic.name,
        len(posts),
        output_path,
    )
    return output_path
