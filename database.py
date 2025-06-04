import json
import os
import uuid

DB_FILE = "files.json"

def _load_db():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        return json.load(f)

def _save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def save_file(file_id, title, size, quality, caption):
    db = _load_db()
    db.append({
        "id": str(uuid.uuid4())[:8],
        "file_id": file_id,
        "title": title,
        "size": f"{round(size / (1024 * 1024), 2)} MB",
        "quality": quality,
        "caption": caption or "📽 Movie"
    })
    _save_db(db)

def search_file_by_name(query):
    db = _load_db()
    return [x for x in db if query.lower() in x['title'].lower()][:10]

def get_file_by_id(file_id):
    db = _load_db()
    for item in db:
        if item["id"] == file_id:
            return item
    return None
