from flask import Flask, render_template_string
import feedparser
import random

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>まとめニュース</title>

<style>
body {
    background:#0d1117;
    color:#e6edf3;
    font-family:"Hiragino Kaku Gothic ProN", sans-serif;
}

.container {
    width:800px;
    margin:0 auto;
}

.card {
    background:#161b22;
    padding:15px;
    margin-bottom:12px;
    border-radius:10px;
    border:1px solid #30363d;
    transition:0.2s;
}

.card:hover {
    transform:scale(1.02);
    border-color:#58a6ff;
}

a {
    color:#58a6ff;
    text-decoration:none;
    font-size:17px;
}

small {
    color:#8b949e;
}
</style>

</head>

<body>
<div class="container">

<h1>最新まとめニュース</h1>

{% for post in posts %}
<div class="card">
    <a href="{{post.link}}" target="_blank">{{post.title}}</a>
    <br>
    <small>{{post.site}}</small>
</div>
{% endfor %}

</div>
</body>
</html>
"""


# --- RSS取得関数 ---
def get_rss(url, name):
    feed = feedparser.parse(url)
    posts = []

    for entry in feed.entries:
        posts.append({
            "title": entry.title,
            "link": entry.link,
            "site": name
        })

    return posts


@app.route("/")
def index():

    posts = []

    # Googleニュース
    posts += get_rss(
        "https://news.google.com/rss?hl=ja&gl=JP&ceid=JP:ja",
        "Googleニュース"
    )

    # Yahooニュース
    posts += get_rss(
        "https://news.yahoo.co.jp/rss/topics/top-picks.xml",
        "Yahooニュース"
    )

    # livedoorニュース
    posts += get_rss(
        "http://news.livedoor.com/topics/rss/top.xml",
        "livedoorニュース"
    )

    # シャッフル（ランダム化）
    random.shuffle(posts)

    # 10件だけ
    posts = posts[:10]

    return render_template_string(HTML, posts=posts)


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)