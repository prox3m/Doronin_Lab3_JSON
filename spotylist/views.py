from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from pathlib import Path
import json, os, re

DATA_FILE = Path(settings.BASE_DIR) / 'data' / 'albums.json'
TIME_RE = re.compile(r'^(\d+:)?\d{1,2}:\d{1,2}:\d{1,2}$')

def index(request):
    albums = read_albums()

    for album in albums:
        if album.get('image'):
            album['image_url'] = f'/media/{album["image"]}'
        else:
            album['image_url'] = '/static/spotylist/images/undefined.jpeg'

    return render(request, 'spotylist/index.html', {'albums': albums})

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

def create_album(request):
    if request.method != 'POST':
        return redirect('index')

    album_data = {
        'name': request.POST.get('name', '').strip(),
        'image': '',
        'authors': request.POST.get('authors', '').strip(),
        'length': request.POST.get('length', '').strip(),
        'tracks': request.POST.getlist('tracks'),
    }

    errors = validate(album_data)
    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect('index')
    
    albums = read_albums()
    album_data['index'] = max((a.get('index', -1) for a in albums), default=-1) + 1
    albums.append(album_data)
    write_albums(albums)

    messages.success(request, f'Альбом ◄{album_data["name"]}► сохранен!')
    return redirect('index')

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

def write_albums(albums):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    text = json.dumps(albums, ensure_ascii=False, indent=4)
    DATA_FILE.write_text(text, encoding="utf-8")