from django.shortcuts import render
from django.conf import settings
from pathlib import Path
import json

DATA_FILE = Path(settings.BASE_DIR) / 'data' / 'albums.json'

def index(request):
    return render(request, 'spotylist/index.html', {'albums': []})
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


def write_albums():
    return []

def validate():
    return []