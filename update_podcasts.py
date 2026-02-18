import feedparser
import datetime
import os
from time import mktime

# 播客配置
PODCASTS = [
    {"name": "Lex Fridman Podcast", "url": "https://lexfridman.com/feed/podcast/", "color": "bg-blue-600"},
    {"name": "Dwarkesh Podcast", "url": "https://www.dwarkeshpatel.com/feed", "color": "bg-indigo-700"},
    {"name": "The Cognitive Revolution", "url": "https://feeds.fireside.fm/cognitive-revolution/rss", "color": "bg-purple-600"},
    {"name": "Lenny's Podcast", "url": "https://api.substack.com/feed/podcast/23337.rss", "color": "bg-pink-600"}
]

def get_podcasts():
    bj_now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    six_months_ago = bj_now - datetime.timedelta(days=180)
    
    all_episodes = []
    
    for pod in PODCASTS:
        try:
            feed = feedparser.parse(pod['url'])
            for entry in feed.entries:
                # 获取发布时间并转为 datetime 格式
                dt = datetime.datetime.fromtimestamp(mktime(entry.published_parsed)) + datetime.timedelta(hours=8)
                
                # 只保留过去 180 天的内容
                if dt > six_months_ago:
                    all_episodes.append({
                        "pod_name": pod['name'],
                        "pod_color": pod['color'],
                        "title": entry.title,
                        "link": entry.link,
                        "date": dt.strftime('%Y-%m-%d'),
                        "timestamp": dt
                    })
        except Exception as e:
            print(f"Error fetching {pod['name']}: {e}")
            
    # 按时间倒序排序（最新的在最上面）
    all_episodes.sort(key=lambda x: x['timestamp'], reverse=True)
    return all_episodes, bj_now.strftime('%Y-%m-%d %H:%M')

episodes, update_time = get_podcasts()

html_cards = ""
for ep in episodes:
    html_cards += f"""
    <div class="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow duration-300 overflow-hidden border border-gray-100">
        <div class="p-5">
            <div class="flex items-center mb-3">
                <span class="inline-block w-3 h-3 rounded-full {ep['pod_color']} mr-2"></span>
                <span class="text-xs font-bold uppercase tracking-wider text-gray-500">{ep['pod_name']}</span>
            </div>
            <h3 class="text-lg font-bold text-gray-900 leading-tight mb-2">
                <a href="{ep['link']}" target="_blank" class="hover:text-blue-600 transition-colors">
                    {ep['title']}
                </a>
            </h3>
            <div class="flex items-center text-sm text-gray-400 mt-4">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                {ep['date']}
            </div>
        </div>
        <div class="bg-gray-50 px-5 py-3 border-t border-gray-100">
            <a href="{ep['link']}" target="_blank" class="text-blue-600 text-sm font-semibold hover:underline">立即收听 →</a>
        </div>
    </div>
    """

full_html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>播客早报 | Podcast Daily</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        body {{ font-family: 'Inter', sans-serif; background-color: #f8fafc; }}
    </style>
</head>
<body class="antialiased text-slate-900">
    <nav class="bg-white border-b border-slate-200 sticky top-0 z-10">
        <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between h-16 items-center">
            <div class="flex items-center">
                <span class="text-2xl mr-2">🎙️</span>
                <span class="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">Podcast Daily</span>
            </div>
            <div class="text-xs text-slate-400">最后更新: {update_time}</div>
        </div>
    </nav>
    <main class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <header class="mb-10 text-center">
            <h1 class="text-3xl font-extrabold text-slate-900 mb-3">半年精选 & 每日追踪</h1>
            <p class="text-lg text-slate-600">过去 180 天的深度对话精华</p>
        </header>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {html_cards}
        </div>
        <footer class="mt-20 pb-10 text-center text-slate-400 text-sm border-t border-slate-200 pt-8">
            <p>由 AI 自动驱动更新 · 每天早上 8:00 定时抓取</p>
        </footer>
    </main>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(full_html)
