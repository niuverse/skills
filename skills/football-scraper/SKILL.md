---
name: football-scraper
description: |
  Chinese football platform scrapers for Hupu, Dongqiudi, and Zhibo8.
  
  Features:
  - Real-time data scraping from major Chinese football platforms
  - Comment extraction with faction analysis (positive vs negative)
  - Rate limiting and anti-detection measures
  - Multi-platform concurrent fetching
  
  Platforms:
  - 虎扑 (Hupu): Largest football community with rich discussions
  - 懂球帝 (Dongqiudi): Professional football news and data
  - 直播吧 (Zhibo8): Live scores and breaking news
  
  Triggers: football scraper, 足球爬虫, 虎扑, 懂球帝, 直播吧, hupu, dongqiudi, zhibo8
---

# Football Scraper Skill

中国足球平台爬虫技能 - 虎扑、懂球帝、直播吧

## Overview

This skill provides real-time data scraping from major Chinese football platforms:
- **虎扑 (Hupu)**: Largest football community, rich discussions
- **懂球帝 (Dongqiudi)**: Professional football news and data  
- **直播吧 (Zhibo8)**: Live scores and breaking news

## Architecture

```
scrapers/
├── base.py          # Abstract base class with rate limiting
├── hupu.py          # Hupu forum scraper
├── dongqiudi.py     # Dongqiudi news API scraper
└── zhibo8.py        # Zhibo8 hot news scraper
```

## Base Scraper Features

- Rate limiting (default: 1 req/sec)
- Timeout handling (default: 15s)
- Session reuse
- Thread-safe throttling

## Platform-Specific Implementation

### HupuScraper
```python
from scrapers.hupu import HupuScraper

scraper = HupuScraper()
posts = scraper.search(
    topic='内马尔',
    start_date=date(2013, 1, 1),
    end_date=date(2024, 12, 31),
    keywords=['内马尔', 'Neymar', '马儿'],
    limit=10
)
```

**Data Source**: `https://bbs.hupu.com/search?q={query}`
**Returns**: Thread title, URL, author, date, likes, replies

### DongqiudiScraper
```python
from scrapers.dongqiudi import DongqiudiScraper

scraper = DongqiudiScraper()
posts = scraper.search(
    topic='梅西',
    keywords=['梅西', 'Messi'],
    limit=10
)
```

**Data Source**: `https://api.dongqiudi.com/search`
**Returns**: News articles with title, URL, likes, comments

### Zhibo8Scraper
```python
from scrapers.zhibo8 import Zhibo8Scraper

scraper = Zhibo8Scraper()
posts = scraper.search(
    topic='世界杯',
    keywords=['世界杯', 'World Cup'],
    limit=10
)
```

**Data Source**: `https://m.zhibo8.cc/json/hot/24hours.htm`
**Returns**: Hot news from last 24 hours

## Data Model

```python
class Post(BaseModel):
    id: str
    topic_id: str
    topic_name: str
    source: str           # "hupu" | "dongqiudi" | "zhibo8"
    source_url: str
    posted_at: datetime
    title: str
    content: str
    author: str
    likes: int
    replies: int
    comments: list[Comment]  # User comments

class Comment(BaseModel):
    id: str
    content: str
    author: str
    posted_at: datetime
    likes: int
```

## Comment Analysis

The scraper now supports **comment content analysis** with faction detection:

```python
# Comments are categorized by sentiment
positive_comments = [...]  # 好、强、棒、赞、支持
negative_comments = [...]  # 差、烂、反对、失望
neutral_comments = [...]   # Other opinions
```

This enables:
- **Faction identification**: Pro-Team A vs Pro-Team B
- **Sentiment intensity**: Measuring emotional strength
- **Representative quotes**: Extracting authentic user voices

## Anti-Detection Measures

1. **User-Agent Rotation**: Real browser UA strings
2. **Rate Limiting**: 1 request per second default
3. **Session Persistence**: Cookie reuse across requests
4. **Request Headers**: Complete browser fingerprint

## Error Handling

- Network timeout: Returns empty list, logs warning
- Rate limit: Automatic backoff
- Parse error: Skips item, continues processing
- No results: Returns empty list

## Usage Example

```python
import asyncio
from scrapers import get_scraper

async def fetch_all_platforms(topic: str):
    platforms = ['hupu', 'dongqiudi', 'zhibo8']
    results = {}
    
    for platform in platforms:
        scraper = get_scraper(platform)
        try:
            posts = await asyncio.to_thread(
                scraper.search,
                topic=topic,
                start_date=None,
                end_date=None,
                limit=20
            )
            # Fetch comments for each post
            for post in posts:
                comments = await asyncio.to_thread(
                    scraper.get_comments,
                    post.id,
                    limit=100  # Up to 100 comments per post
                )
                post.comments = comments
            results[platform] = posts
        finally:
            scraper.close()
    
    return results
```

## Testing

```bash
# Test all scrapers
python -c "
from scrapers.hupu import HupuScraper
scraper = HupuScraper()
posts = scraper.search('内马尔', None, None, limit=5)
print(f'Found {len(posts)} posts')
for p in posts:
    print(f'  - {p.title[:50]}...')
"
```

## Limitations

- **Comments**: Some platforms require browser automation for full comment extraction
- **Historical data**: Limited by platform search/indexing
- **Rate limits**: Platforms may block aggressive scraping
- **Content**: Some text may need HTML cleaning

## Performance

With the enhanced comment extraction:
- **Posts per search**: 5-10 posts
- **Comments per post**: 50-100 comments
- **Total data points**: 500-1000 comments per topic

## References

- Hupu: https://bbs.hupu.com
- Dongqiudi: https://www.dongqiudi.com
- Zhibo8: https://www.zhibo8.cc
