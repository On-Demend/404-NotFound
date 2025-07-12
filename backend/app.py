from flask import Flask, request, jsonify
from utils.config_generator import generate_config
import subprocess
import os

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        config_path = generate_config(data)

        # GitHub Actions 트리거 (로컬에선 시뮬레이션)
        # 또는 subprocess.run([...])으로 aws-nuke 직접 실행

        return jsonify({"status": "started", "config_path": config_path})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
