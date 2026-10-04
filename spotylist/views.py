from django.shortcuts import render
from django.conf import settings
from pathlib import Path
import json, os

DATA_FILE = Path(settings.BASE_DIR) / 'data' / 'albums.json'
TIME_RE = re.compile(r'^(\d+:)?\d{1,2}:\d{2}:\d{2}$')

def index(request):
    return render(request, 'spotylist/index.html', {'albums': []})

def read_albums():
    if not DATA_FILE.exists():
        return []

    file_text = DATA_FILE.read_text(encoding='utf-8').strip()
    if not file_text:
        return []

    try:
        return json.loads(file_text)
    except json.JSONDecodeError as e:
        print(e)
        return []


def write_albums(albums):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    text = json.dumps(albums, ensure_ascii=False, indent=4)
    DATA_FILE.write_text(text, encoding="utf-8")


def validate():
    return []