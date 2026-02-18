import feedparser
import datetime
import os

# 播客配置（你可以随时增加新的，只需填入名字、RSS地址和图标颜色）
PODCASTS = [
    {"name": "Lex Fridman Podcast", "url": "https://lexfridman.com/feed/podcast/", "color": "bg-blue-600"},
    {"name": "Dwarkesh Podcast", "url": "https://www.dwarkeshpatel.com/feed", "color": "bg-indigo-700"},
    {"name": "The Cognitive Revolution", "url": "https://feeds.fireside.fm/cognitive-revolution/rss", "color": "bg-purple-600"},
    {"name": "Lenny's Podcast", "url": "https://api.substack.com/feed/podcast/23337.rss", "color": "bg-pink-600"}
]

def get_latest_episodes():
    # 获取北京时间
    bj_now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    update_time = bj_now.strftime('%Y-%m-%d %H:%M')
    
    html_cards = ""
    
    for pod in PODCASTS:
        try:
            feed = feedparser.parse(pod['url'])
            # 每个播客显示最近 3 集，保持页面整洁
            for entry in feed.entries[:3]:
                # 尝试获取日期
                date_str = entry.published if 'published' in entry else ""
                # 简单处理日期显示，只保留年月日
                short_date = date_str[:16] if date_str else "最近更新"
                
                # 生成精美的 HTML 卡片
                html_cards += f"""
                <div class="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow duration-300 overflow-hidden border border-gray-100">
                    <div class="p-5">
                        <div class="flex items-center mb-3">
                            <span class="inline-block w-3 h-3 rounded-full {pod['color']} mr-2"></span>
                            <span class="text-xs font-bold uppercase tracking-wider text-gray-500">{pod['name']}</span>
                        </div>
                        <h3 class="text-lg font-bold text-gray-900 leading-tight mb-2">
                            <a href="{entry.link}" target="_blank" class="hover:text-blue-600 transition-colors">
                                {entry.title}
                            </a>
                        </h3>
                        <div class="flex items-center text-sm text-gray-400 mt-4">
                            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="Wait, what?"></path>
                                <path d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                            </svg>
                            {short_date}
                        </div>
                    </div>
                    <div class="bg-gray-50 px-5 py-3 border-t border-gray-100 flex justify-between items-center">
                        <a href="{entry.link}" target="_blank" class="text-blue-600 text-sm font-semibold hover:underline">立即收听 →</a>
                    </div>
                </div>
                """
        except Exception as e:
            continue
            
    return html_cards, update_time

cards_html, last_update = get_latest_episodes()

# 使用 Tailwind CSS 构建的高级 HTML 模版
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
    <!-- 导航栏 -->
    <nav class="bg-white border-b border-slate-200 sticky top-0 z-10">
        <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16 items-center">
                <div class="flex items-center">
                    <span class="text-2xl mr-2">🎙️</span>
                    <span class="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">
                        Podcast Daily
                    </span>
                </div>
                <div class="text-xs text-slate-400">
                    最后更新: {last_update}
                </div>
            </div>
        </div>
    </nav>

    <!-- 主体内容 -->
    <main class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <header class="mb-10 text-center">
            <h1 class="text-3xl font-extrabold text-slate-900 sm:text-4xl mb-3">
                你想听的，都在这里
            </h1>
            <p class="text-lg text-slate-600">
                聚合 Lex Fridman, Dwarkesh, Cognitive Revolution 和 Lenny's Podcast 的最新动态。
            </p>
        </header>

        <!-- 卡片网格 -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {cards_html}
        </div>

        <footer class="mt-20 pb-10 text-center text-slate-400 text-sm border-t border-slate-200 pt-8">
            <p>由 AI 自动驱动更新 · 每天早上 8:00 准时推送</p>
        </footer>
    </main>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(full_html)
