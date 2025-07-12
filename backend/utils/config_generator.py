import yaml
import uuid

def generate_config(data):
    config = {
        "regions": data["regions"] + ["global"],
        "account-blocklist": [data["excludeId"]] if data["excludeId"] else [],
        "accounts": {
            data["accountId"]: {
                "aliases": [data["alias"]],
                "filters": {
                    "IAMUser": [data["iamUser"]],
                    "IAMUserLoginProfile": [data["iamProfile"]]
                }
            }
        }
    }

    path = f"/tmp/nuke-config-{uuid.uuid4().hex}.yaml"
    with open(path, "w") as f:
        yaml.dump(config, f)
    return path
