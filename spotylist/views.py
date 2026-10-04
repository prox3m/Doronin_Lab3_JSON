from django.shortcuts import render
from django.conf import settings
from pathlib import Path
import json, os, re

DATA_FILE = Path(settings.BASE_DIR) / 'data' / 'albums.json'
TIME_RE = re.compile(r'^(\d+:)?\d{1,2}:\d{1,2}:\d{1,2}$')

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
    except json.JSONDecodeError:
        return []


def write_albums(albums):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    text = json.dumps(albums, ensure_ascii=False, indent=4)
    DATA_FILE.write_text(text, encoding="utf-8")


def validate(album):
    not_valid = []

    name = album.get('name', '')
    if name.strip() == '':
        not_valid.append('Название обязательно')
    
    length = album.get('length', '')
    if length != '':
        if not TIME_RE.match(length):
            not_valid.append('Неверный формат времени')
    
    tracks = album.get('tracks', [])

    if type(tracks) is list:
        for i, track in enumerate(tracks):
            if not track.strip():
                not_valid.append(f"Пустой трек №{i + 1} в списке")
    else:
        not_valid.append("Треки должны быть списком")
    
    return not_valid