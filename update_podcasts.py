import feedparser
import datetime
import os

# 播客 RSS 列表
PODCASTS = {
    "Lex Fridman": "https://lexfridman.com/feed/podcast/",
    "Dwarkesh Podcast": "https://www.dwarkeshpatel.com/feed",
    "The Cognitive Revolution": "https://feeds.fireside.fm/cognitive-revolution/rss",
    "Lenny's Podcast": "https://api.substack.com/feed/podcast/23337.rss"
}

def get_latest_episodes():
    # 获取当前北京时间 (UTC+8)
    utc_now = datetime.datetime.utcnow()
    bj_now = utc_now + datetime.timedelta(hours=8)
    
    content = f"<h1>我的播客追踪器</h1><p>最后更新时间 (北京时间): {bj_now.strftime('%Y-%m-%d %H:%M')}</p>"
    
    for name, url in PODCASTS.items():
        try:
            feed = feedparser.parse(url)
            content += f"<h2>{name}</h2><ul>"
            # 取最近 10 集
            for entry in feed.entries[:10]:
                date = entry.published if 'published' in entry else "未知日期"
                content += f"<li>[{date}] - <a href='{entry.link}' target='_blank'><strong>{entry.title}</strong></a></li>"
            content += "</ul>"
        except Exception as e:
            content += f"<h2>{name}</h2><p>抓取失败: {e}</p>"
    
    return content

html_template = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>播客每日追踪</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.6; max-width: 900px; margin: auto; padding: 20px; background: #f9f9f9; color: #333; }}
        h1 {{ text-align: center; color: #1a1a1a; border-bottom: 3px solid #007bff; padding-bottom: 10px; }}
        h2 {{ color: #007bff; border-left: 5px solid #007bff; padding-left: 10px; margin-top: 40px; }}
        ul {{ list-style: none; padding: 0; }}
        li {{ background: white; margin-bottom: 10px; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
        a {{ text-decoration: none; color: #1a0dab; font-size: 1.1em; }}
        a:hover {{ text-decoration: underline; }}
        p {{ color: #666; }}
    </style>
</head>
<body>
    {get_latest_episodes()}
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_template)
