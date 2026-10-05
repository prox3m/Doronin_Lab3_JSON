const trackInput = document.getElementById('track-input');
const addButton = document.getElementById('add-track-btn');
const trackList = document.getElementById('track-list-edit');

addButton.addEventListener('click', function () {
    const trackName = trackInput.value.trim();

    if (!trackName) {
        return;
    }

    const row = document.createElement('div');
    row.className = 'track-edit-row';

    const name = document.createElement('span');
    name.className = 'track-edit-name';
    name.textContent = trackName;

    const button = document.createElement('button');
    button.className = 'remove-track';
    button.textContent = 'X';
    button.addEventListener('click', function() {
        row.remove();
    });

    row.appendChild(name);
    row.appendChild(button);

    trackList.appendChild(row);
    trackInput.value = '';
});