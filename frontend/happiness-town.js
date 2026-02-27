// ====== VIDEO OVERLAYS ======
const danceOverlay = document.getElementById('danceOverlay');
const danceCloseBtn = document.getElementById('danceCloseBtn');
const danceVideo = document.getElementById('danceVideo');
const danceBtn = document.getElementById('danceBtn');

const comedyOverlay = document.getElementById('comedyOverlay');
const comedyCloseBtn = document.getElementById('comedyCloseBtn');
const comedyVideo = document.getElementById('comedyVideo');
const comedyBtn = document.getElementById('comedyBtn');

const affirmationsOverlay = document.getElementById('affirmationsOverlay');
const affirmationsCloseBtn = document.getElementById('affirmationsCloseBtn');
const affirmationsVideo = document.getElementById('affirmationsVideo');
const affirmationsBtn = document.getElementById('affirmationsBtn');

const upbeatMusicOverlay = document.getElementById('upbeatMusicOverlay');
const upbeatMusicCloseBtn = document.getElementById('upbeatMusicCloseBtn');
const upbeatMusicVideo = document.getElementById('upbeatMusicVideo');
const upbeatMusicBtn = document.getElementById('upbeatMusicBtn');

// ====== DANCE PARTY ======
function openDance() {
  document.getElementById('danceSpinner').style.display = 'block';
  document.getElementById('danceVideo').style.display = 'none';
  danceVideo.src = 'https://www.youtube.com/embed/gCzgc_RelBA?autoplay=1';
  danceVideo.setAttribute(
    'allow',
    'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share',
  );
  danceVideo.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin');
  danceOverlay.hidden = false;
  danceVideo.onload = function () {
    document.getElementById('danceSpinner').style.display = 'none';
    document.getElementById('danceVideo').style.display = 'block';
  };
}

function closeDance() {
  danceVideo.src = '';
  danceOverlay.hidden = true;
}

if (danceBtn) danceBtn.addEventListener('click', openDance);
if (danceCloseBtn) danceCloseBtn.addEventListener('click', closeDance);

// ====== COMEDY BREAK ======
function openComedy() {
  document.getElementById('comedySpinner').style.display = 'block';
  document.getElementById('comedyVideo').style.display = 'none';
  comedyVideo.src = 'https://www.youtube.com/embed/Z4C82eyhwgU?autoplay=1';
  comedyVideo.setAttribute(
    'allow',
    'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share',
  );
  comedyVideo.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin');
  comedyOverlay.hidden = false;
  comedyVideo.onload = function () {
    document.getElementById('comedySpinner').style.display = 'none';
    document.getElementById('comedyVideo').style.display = 'block';
  };
}

function closeComedy() {
  comedyVideo.src = '';
  comedyOverlay.hidden = true;
}

if (comedyBtn) comedyBtn.addEventListener('click', openComedy);
if (comedyCloseBtn) comedyCloseBtn.addEventListener('click', closeComedy);

// ====== POSITIVE AFFIRMATIONS ======
function openAffirmations() {
  document.getElementById('affirmationsSpinner').style.display = 'block';
  document.getElementById('affirmationsVideo').style.display = 'none';
  affirmationsVideo.src = 'https://www.youtube.com/embed/z0He0Bp45C4?autoplay=1';
  affirmationsVideo.setAttribute(
    'allow',
    'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share',
  );
  affirmationsVideo.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin');
  affirmationsOverlay.hidden = false;
  affirmationsVideo.onload = function () {
    document.getElementById('affirmationsSpinner').style.display = 'none';
    document.getElementById('affirmationsVideo').style.display = 'block';
  };
}

function closeAffirmations() {
  affirmationsVideo.src = '';
  affirmationsOverlay.hidden = true;
}

if (affirmationsBtn) affirmationsBtn.addEventListener('click', openAffirmations);
if (affirmationsCloseBtn) affirmationsCloseBtn.addEventListener('click', closeAffirmations);

// ====== UPBEAT MUSIC ======
function openUpbeatMusic() {
  document.getElementById('upbeatMusicSpinner').style.display = 'block';
  document.getElementById('upbeatMusicVideo').style.display = 'none';
  upbeatMusicVideo.src = 'https://www.youtube.com/embed/y6Sxv-sUYtM?autoplay=1';
  upbeatMusicVideo.setAttribute(
    'allow',
    'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share',
  );
  upbeatMusicVideo.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin');
  upbeatMusicOverlay.hidden = false;
  upbeatMusicVideo.onload = function () {
    document.getElementById('upbeatMusicSpinner').style.display = 'none';
    document.getElementById('upbeatMusicVideo').style.display = 'block';
  };
}

function closeUpbeatMusic() {
  upbeatMusicVideo.src = '';
  upbeatMusicOverlay.hidden = true;
}

if (upbeatMusicBtn) upbeatMusicBtn.addEventListener('click', openUpbeatMusic);
if (upbeatMusicCloseBtn) upbeatMusicCloseBtn.addEventListener('click', closeUpbeatMusic);

// ====== SHARE YOUR HAPPINESS & POSITIVITY BOARD ======
const API_BASE =
  window.location.origin.includes('localhost:8000') || window.location.origin.includes('127.0.0.1:8000')
    ? window.location.origin
    : 'http://127.0.0.1:8000';

const USER_ID_STORAGE_KEY = 'moodSwingsUserId';
const noteInput = document.getElementById('happy-note');
const submitButton = document.getElementById('happy-submit');
const submitStatus = document.getElementById('submit-status');
const boardStatus = document.getElementById('board-status');
const boardList = document.getElementById('positivity-board');

async function ensureUserId() {
  const storedId = localStorage.getItem(USER_ID_STORAGE_KEY);
  if (storedId) {
    return storedId;
  }

  const response = await fetch(`${API_BASE}/users`, { method: 'POST' });
  if (!response.ok) {
    throw new Error('Unable to create user session.');
  }

  const data = await response.json();
  localStorage.setItem(USER_ID_STORAGE_KEY, data.id);
  return data.id;
}

function renderNotes(notes) {
  boardList.innerHTML = '';

  if (!notes.length) {
    const emptyItem = document.createElement('li');
    emptyItem.className = 'positivity-empty';
    emptyItem.textContent = 'No notes yet. Be the first to spread positivity.';
    boardList.appendChild(emptyItem);
    return;
  }

  notes.forEach((note) => {
    const item = document.createElement('li');
    item.className = 'positivity-note';
    item.textContent = `✨ ${note.note}`;
    boardList.appendChild(item);
  });
}

async function loadPositivityBoard(userId) {
  boardStatus.textContent = 'Loading positivity board...';

  try {
    const response = await fetch(`${API_BASE}/notes/latest?user_id=${encodeURIComponent(userId)}`);
    if (!response.ok) {
      throw new Error('Failed to load notes.');
    }

    const notes = await response.json();
    renderNotes(notes);
    boardStatus.textContent = '';
  } catch (error) {
    boardStatus.textContent = 'Unable to load notes from the backend right now.';
    renderNotes([]);
  }
}

async function submitHappyNote() {
  const note = noteInput.value.trim();

  if (!note) {
    submitStatus.textContent = 'Please write something before submitting.';
    return;
  }

  submitButton.disabled = true;
  submitStatus.textContent = 'Saving your note...';

  try {
    const userId = await ensureUserId();
    const response = await fetch(`${API_BASE}/notes?user_id=${encodeURIComponent(userId)}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ note }),
    });

    if (!response.ok) {
      throw new Error('Failed to save note.');
    }

    noteInput.value = '';
    submitStatus.textContent = 'Your positive note has been shared.';
    await loadPositivityBoard(userId);
  } catch (error) {
    submitStatus.textContent = 'Could not save your note. Please try again.';
  } finally {
    submitButton.disabled = false;
  }
}

if (submitButton) submitButton.addEventListener('click', submitHappyNote);

(async () => {
  try {
    const userId = await ensureUserId();
    await loadPositivityBoard(userId);
  } catch (error) {
    boardStatus.textContent = 'Unable to connect to backend. Start FastAPI and refresh.';
    renderNotes([]);
  }
})();
