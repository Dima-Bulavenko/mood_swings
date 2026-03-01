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

// Destroys the iframe when the modal closes (guaranteed media stop) and recreates it on open.
function setupModalMediaReset(modalId) {
  const modalElement = document.getElementById(modalId);
  if (!modalElement) return;

  const container = modalElement.querySelector('.ratio');
  if (!container) return;

  const templateIframe = container.querySelector('iframe');
  if (!templateIframe) return;

  const embedSrc = templateIframe.getAttribute('data-embed-src') || '';
  if (!embedSrc) return;

  // Stores original iframe attributes to recreate it identically each time.
  const savedAttrs = {};
  Array.from(templateIframe.attributes).forEach(function (attr) {
    savedAttrs[attr.name] = attr.value;
  });

  modalElement.addEventListener('shown.bs.modal', function () {
    const newIframe = document.createElement('iframe');
    Object.keys(savedAttrs).forEach(function (name) {
      if (name !== 'src') newIframe.setAttribute(name, savedAttrs[name]);
    });
    // Sets src last so the browser loads the video only when modal is fully visible.
    newIframe.src = embedSrc;
    container.innerHTML = '';
    container.appendChild(newIframe);
  });

  // Removes the iframe entirely from the DOM, destroying the audio context.
  modalElement.addEventListener('hide.bs.modal', function () {
    container.innerHTML = '';
  });
}

setupModalMediaReset('danceModal');
setupModalMediaReset('comedyModal');
setupModalMediaReset('upbeatMusicModal');

setupModalMediaReset('danceModal');
setupModalMediaReset('comedyModal');
setupModalMediaReset('upbeatMusicModal');

// ====== DANCE PARTY ======
function openDance() {
  const danceSpinner = document.getElementById('danceSpinner');
  danceSpinner.style.display = 'block';
  danceVideo.style.display = 'block';
  danceVideo.src = 'https://www.youtube.com/embed/gCzgc_RelBA?autoplay=1';
  danceVideo.setAttribute(
    'allow',
    'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share',
  );
  danceVideo.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin');
  danceOverlay.hidden = false;
  // Fallback hides spinner even if iframe load event is delayed.
  window.setTimeout(function () {
    danceSpinner.style.display = 'none';
  }, 1200);
  danceVideo.onload = function () {
    danceSpinner.style.display = 'none';
    danceVideo.style.display = 'block';
  };
}

function closeDance() {
  danceVideo.src = '';
  document.getElementById('danceSpinner').style.display = 'none';
  danceOverlay.hidden = true;
}

if (danceBtn)
  danceBtn.addEventListener('click', function (event) {
    event.preventDefault();
    openDance();
  });
if (danceCloseBtn) danceCloseBtn.addEventListener('click', closeDance);

// ====== COMEDY BREAK ======
function openComedy() {
  const comedySpinner = document.getElementById('comedySpinner');
  comedySpinner.style.display = 'block';
  comedyVideo.style.display = 'block';
  comedyVideo.src = 'https://www.youtube.com/embed/Z4C82eyhwgU?autoplay=1';
  comedyVideo.setAttribute(
    'allow',
    'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share',
  );
  comedyVideo.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin');
  comedyOverlay.hidden = false;
  // Fallback hides spinner even if iframe load event is delayed.
  window.setTimeout(function () {
    comedySpinner.style.display = 'none';
  }, 1200);
  comedyVideo.onload = function () {
    comedySpinner.style.display = 'none';
    comedyVideo.style.display = 'block';
  };
}

function closeComedy() {
  comedyVideo.src = '';
  document.getElementById('comedySpinner').style.display = 'none';
  comedyOverlay.hidden = true;
}

if (comedyBtn)
  comedyBtn.addEventListener('click', function (event) {
    event.preventDefault();
    openComedy();
  });
if (comedyCloseBtn) comedyCloseBtn.addEventListener('click', closeComedy);

// ====== POSITIVE AFFIRMATIONS ======
function openAffirmations() {
  const affirmationsSpinner = document.getElementById('affirmationsSpinner');
  affirmationsSpinner.style.display = 'block';
  affirmationsVideo.style.display = 'block';
  affirmationsVideo.src = 'https://www.youtube.com/embed/z0He0Bp45C4?autoplay=1';
  affirmationsVideo.setAttribute(
    'allow',
    'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share',
  );
  affirmationsVideo.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin');
  affirmationsOverlay.hidden = false;
  // Fallback hides spinner even if iframe load event is delayed.
  window.setTimeout(function () {
    affirmationsSpinner.style.display = 'none';
  }, 1200);
  affirmationsVideo.onload = function () {
    affirmationsSpinner.style.display = 'none';
    affirmationsVideo.style.display = 'block';
  };
}

function closeAffirmations() {
  affirmationsVideo.src = '';
  document.getElementById('affirmationsSpinner').style.display = 'none';
  affirmationsOverlay.hidden = true;
}

if (affirmationsBtn)
  affirmationsBtn.addEventListener('click', function (event) {
    event.preventDefault();
    openAffirmations();
  });
if (affirmationsCloseBtn) affirmationsCloseBtn.addEventListener('click', closeAffirmations);

// ====== UPBEAT MUSIC ======
function openUpbeatMusic() {
  const upbeatMusicSpinner = document.getElementById('upbeatMusicSpinner');
  upbeatMusicSpinner.style.display = 'block';
  upbeatMusicVideo.style.display = 'block';
  upbeatMusicVideo.src = 'https://www.youtube.com/embed/FcYp2AZUl1Q?enablejsapi=1';
  upbeatMusicVideo.setAttribute('allow', 'accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture');
  upbeatMusicVideo.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin');
  upbeatMusicOverlay.hidden = false;
  // Fallback hides spinner even if iframe load event is delayed.
  window.setTimeout(function () {
    upbeatMusicSpinner.style.display = 'none';
  }, 1200);
  upbeatMusicVideo.onload = function () {
    upbeatMusicSpinner.style.display = 'none';
    upbeatMusicVideo.style.display = 'block';
  };
}

function closeUpbeatMusic() {
  upbeatMusicVideo.src = '';
  document.getElementById('upbeatMusicSpinner').style.display = 'none';
  upbeatMusicOverlay.hidden = true;
}

if (upbeatMusicBtn)
  upbeatMusicBtn.addEventListener('click', function (event) {
    event.preventDefault();
    openUpbeatMusic();
  });
if (upbeatMusicCloseBtn) upbeatMusicCloseBtn.addEventListener('click', closeUpbeatMusic);

// ====== SHARE YOUR HAPPINESS & POSITIVITY BOARD ======
const client = window.MoodSwingsClient.createClient();
const noteInput = document.getElementById('happy-note');
const noteLabel = document.querySelector('label[for="happy-note"]');
const noteHelp = document.getElementById('happy-note-help');
const submitButton = document.getElementById('happy-submit');
const submitStatus = document.getElementById('submit-status');
const boardStatus = document.getElementById('board-status');
const boardList = document.getElementById('positivity-board');
const boardPrevButton = document.getElementById('board-prev');
const boardNextButton = document.getElementById('board-next');
const createAnotherButton = document.createElement('button');
const BOARD_PAGE_SIZE = 5;
let boardOffset = 0;
let boardHasMore = false;

createAnotherButton.type = 'button';
createAnotherButton.className = 'btn btn-outline-primary mt-3 w-100 d-none';
createAnotherButton.id = 'happy-create-another';
createAnotherButton.textContent = 'Create another note';
submitStatus.insertAdjacentElement('afterend', createAnotherButton);

function setSubmitStatus(message, state) {
  submitStatus.textContent = message;
  submitStatus.classList.remove('status-success', 'status-error', 'status-neutral');

  if (state === 'success') {
    submitStatus.classList.add('status-success');
    return;
  }

  if (state === 'error') {
    submitStatus.classList.add('status-error');
    return;
  }

  submitStatus.classList.add('status-neutral');
}

function setNoteComposerVisibility(isVisible) {
  if (noteLabel) noteLabel.classList.toggle('d-none', !isVisible);
  if (noteHelp) noteHelp.classList.toggle('d-none', !isVisible);
  noteInput.classList.toggle('d-none', !isVisible);
  submitButton.classList.toggle('d-none', !isVisible);
  createAnotherButton.classList.toggle('d-none', isVisible);
}

async function ensureUserId() {
  if (typeof window.ensureMoodSwingsUserId !== 'function') {
    throw new Error('ensureMoodSwingsUserId is not available. Include index.js before happiness-town.js.');
  }

  return window.ensureMoodSwingsUserId();
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

  notes.forEach((note, index) => {
    const item = document.createElement('li');
    item.className = 'positivity-note';
    item.style.setProperty('--note-delay', `${index * 60}ms`);
    item.textContent = `✨ ${note.note}`;
    boardList.appendChild(item);
  });
}

function updateBoardPaginationControls() {
  if (boardPrevButton) {
    boardPrevButton.disabled = boardOffset === 0;
  }

  if (boardNextButton) {
    boardNextButton.disabled = !boardHasMore;
  }
}

async function loadPositivityBoard() {
  boardStatus.textContent = 'Loading positivity board...';
  if (boardPrevButton) boardPrevButton.disabled = true;
  if (boardNextButton) boardNextButton.disabled = true;

  try {
    const notes = await client.getLatestNotes({
      limit: BOARD_PAGE_SIZE,
      offset: boardOffset,
    });

    boardHasMore = notes.length === BOARD_PAGE_SIZE;
    renderNotes(notes);
    boardStatus.textContent = '';
    updateBoardPaginationControls();
  } catch (error) {
    boardStatus.textContent = 'Unable to load notes from the backend right now.';
    boardHasMore = false;
    renderNotes([]);
    updateBoardPaginationControls();
  }
}

async function submitHappyNote() {
  const note = noteInput.value.trim();

  if (!note) {
    setSubmitStatus('Please write something before submitting.', 'error');
    return;
  }

  submitButton.disabled = true;
  setSubmitStatus('Saving your note...', 'neutral');

  try {
    const userId = await ensureUserId();
    await client.createNote(userId, note);

    noteInput.value = '';
    setSubmitStatus('Your positive note has been shared.', 'success');
    setNoteComposerVisibility(false);
    boardOffset = 0;
    await loadPositivityBoard();
  } catch (error) {
    setSubmitStatus('Could not save your note. Please try again.', 'error');
  } finally {
    submitButton.disabled = false;
  }
}

if (submitButton) submitButton.addEventListener('click', submitHappyNote);

createAnotherButton.addEventListener('click', function () {
  setNoteComposerVisibility(true);
  setSubmitStatus('', 'neutral');
  noteInput.focus();
});

if (boardPrevButton) {
  boardPrevButton.addEventListener('click', async function () {
    if (boardOffset === 0) return;

    boardOffset = Math.max(0, boardOffset - BOARD_PAGE_SIZE);
    await loadPositivityBoard();
  });
}

if (boardNextButton) {
  boardNextButton.addEventListener('click', async function () {
    if (!boardHasMore) return;

    boardOffset += BOARD_PAGE_SIZE;
    await loadPositivityBoard();
  });
}

(async () => {
  try {
    await ensureUserId();
    boardOffset = 0;
    await loadPositivityBoard();
  } catch (error) {
    boardStatus.textContent = 'Unable to connect to backend. Start FastAPI and refresh.';
    renderNotes([]);
  }
})();
