from flask import Flask, request, send_from_directory, render_template_string
import yt_dlp
import os

app = Flask(__name__)
os.makedirs("downloads", exist_ok=True)

HTML = """
<html>
<head><meta name="google-site-verification" content="KwJ-s4omakls6BGHcU5r05jNjWzXJSpUOeHvqhyEN8U" /><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{background:#111;color:#fff;font-family:sans-serif;text-align:center;padding:20px}
input{width:95%;padding:14px;border-radius:10px;border:none;margin:10px 0}
button{padding:14px 30px;background:#ff0055;color:#fff;border:none;border-radius:10px;font-size:16px}
.card{background:#222;padding:15px;border-radius:12px;margin-top:20px;word-break:break-all}
a{color:#00ff88}
</style>
</head>
<body>
<h1>🔥 Super Downloader v4</h1>
<form method="POST">
<input name="url" placeholder="YouTube / Insta / FB link yahan daalo" required>
<br><button>Download</button>
</form>
<div class="card">{{msg|safe}}</div>
</body>
</html>
"""

@app.route('/', methods=['GET','POST'])
def home():
    msg = "Link daalo aur download karo"
    if request.method == 'POST':
        url = request.form['url']
        try:
            opts = {
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'format': 'best',
                'quiet': True
            }
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                base = os.path.basename(filename)
            msg = f"✅ Ho gaya!<br><a href='/downloads/{base}' download>👉 Yahan click karke save karo: {base}</a>"
        except Exception as e:
            msg = f"❌ Error: {e}"
    return render_template_string(HTML, msg=msg)

@app.route('/downloads/<path:name>')
def dl(name):
    return send_from_directory("downloads", name, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
