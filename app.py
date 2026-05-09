# app.py
# Flask web server - handles all pages and API endpoints

from flask import Flask, render_template, request, jsonify, send_file
import os
from datetime import datetime
from dotenv import load_dotenv
from database import get_all_briefings, get_all_logs, get_briefing_by_date

load_dotenv()
app = Flask(__name__)

# PAGE ROUTES
@app.route("/")
def dashboard():
    today = datetime.now().strftime("%Y-%m-%d")
    briefing = get_briefing_by_date(today)
    return render_template("index.html", briefing=briefing, today=today)

@app.route("/history")
def history():
    briefings = get_all_briefings()
    return render_template("history.html", briefings=briefings)

@app.route("/settings")
def settings():
    prefs = {
        "name": os.getenv("YOUR_NAME", ""),
        "topics": os.getenv("YOUR_TOPICS", ""),
        "telegram_id": os.getenv("TELEGRAM_CHAT_ID", "")
    }
    return render_template("settings.html", prefs=prefs)

@app.route("/logs")
def logs():
    all_logs = get_all_logs()
    return render_template("logs.html", logs=all_logs)

# API ROUTES (called by JavaScript)
@app.route("/api/run", methods=["POST"])
def run_now():
    try:
        from main import run_briefing
        run_briefing()
        return jsonify({"status": "success",
                        "message": "Briefing done! Check Telegram."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/save-settings", methods=["POST"])
def save_settings():
    data = request.get_json()
    env_lines = []
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            env_lines = f.readlines()

    def update(lines, key, val):
        for i, line in enumerate(lines):
            if line.startswith(key + "="):
                lines[i] = f"{key}={val}\n"
                return lines
        lines.append(f"{key}={val}\n")
        return lines

    env_lines = update(env_lines, "YOUR_NAME", data.get("name", ""))
    env_lines = update(env_lines, "YOUR_TOPICS", data.get("topics", ""))
    with open(".env", "w") as f:
        f.writelines(env_lines)
    load_dotenv(override=True)
    return jsonify({"status": "success", "message": "Settings saved!"})

@app.route("/api/audio/<path:filename>")
def serve_audio(filename):
    return send_file(filename, mimetype="audio/mpeg")

@app.route("/api/status")
def status():
    today = datetime.now().strftime("%Y-%m-%d")
    briefing = get_briefing_by_date(today)
    return jsonify({
        "today": today,
        "briefing_ready": briefing is not None,
        "time": datetime.now().strftime("%H:%M:%S")
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)