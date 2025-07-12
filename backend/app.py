from flask import Flask, render_template, request, jsonify
import subprocess
import yaml
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_nuke():
    try:
        data = request.json

        config = {
            "regions": data['regions'] + ["global"],
            "account-blocklist": [data['exclude_id'] or "000000000000"],
            "accounts": {
                data["account_id"]: {
                    "aliases": [data["alias"]],
                    "filters": {
                        "IAMUser": [data["iam_user"]],
                        "IAMUserLoginProfile": [data["iam_profile"]]
                    }
                }
            }
        }

        with open("nuke-config.yaml", "w") as f:
            yaml.dump(config, f)

        env = os.environ.copy()
        env["AWS_ACCESS_KEY_ID"] = data["aws_access_key"]
        env["AWS_SECRET_ACCESS_KEY"] = data["aws_secret_key"]
        env["AWS_REGION"] = data["regions"][0] if data["regions"] else "us-east-1"

        cmd = ["aws-nuke", "-c", "nuke-config.yaml", "--no-dry-run", "--force"]

        result = subprocess.run(cmd, capture_output=True, text=True, env=env)

        if result.returncode == 0:
            return jsonify(success=True)
        else:
            return jsonify(success=False, message=result.stderr or result.stdout)

    except Exception as e:
        return jsonify(success=False, message=str(e))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
