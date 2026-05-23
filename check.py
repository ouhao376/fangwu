import requests
import hashlib
import json
import os

TOKEN = "fc8622dff3434e16aa69ccab198bfb6e"
URL = "https://m.ke.com/chuzu/zufang/rt200600000001/"
STATE_FILE = "state.json"

def push(title, content):
    requests.post("http://www.pushplus.plus/send", json={
        "token": TOKEN,
        "title": title,
        "content": content,
        "template": "html"
    })

def load():
    if not os.path.exists(STATE_FILE):
        return set()
    try:
        return set(json.load(open(STATE_FILE)))
    except:
        return set()

def save(data):
    json.dump(list(data), open(STATE_FILE, "w"))

def fetch():
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    html = r.text

    items = []

    for part in html.split("resblock-list"):
        if "title" in part:
            try:
                title = part.split("title")[1].split('"')[1]
                uid = hashlib.md5(title.encode()).hexdigest()

                items.append({
                    "id": uid,
                    "title": title
                })
            except:
                pass

    return items

def main():
    old = load()
    new = set(old)

    for item in fetch():
        if item["id"] not in old:
            push("🏠 新房源提醒", item["title"])
            new.add(item["id"])

    save(new)

main()
