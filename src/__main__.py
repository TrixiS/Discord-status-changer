import config

import sys
import time
import requests
import itertools
import emoji

with open(config.statuses_path, "r", encoding="utf-8") as f:
    statuses_content = f.read()

statuses = []

for line in statuses_content.splitlines():
    if line.startswith('#'):
        continue

    try:
        status_emoji, *status, wait_time = line.strip().split()

        if len(status) == 0:
            continue

        if status_emoji not in emoji.EMOJI_ALIAS_UNICODE.values():
            status.insert(0, status_emoji)
            status_emoji = None

        statuses.append((status_emoji, ' '.join(status).strip(), int(wait_time)))
    except Exception:
        print(f"Invalid syntax in statuses file: {config.statuses_path}\nUse: <status> <time in seconds>")
        sys.exit()

if len(statuses) == 0:
    print(f"No statuses found in file {config.statuses_path}")
    sys.exit()

for status_emoji, status, wait_time in itertools.cycle(statuses):
    if wait_time <= 0:
        continue

    request_json = {
        "custom_status": {
            "text": status,
            "expires_at": "2020-12-17T19:00:00.000Z"
        }
    }

    if status_emoji is not None:
        request_json["custom_status"]["emoji_name"] = status_emoji

    response = requests.patch(
        "https://discord.com/api/v8/users/@me/settings",
        headers={"authorization": config.account_token},
        json=request_json
    )

    print(f"Set status \"{status_emoji or ''}{status}\" for {wait_time} seconds")
    time.sleep(wait_time)
