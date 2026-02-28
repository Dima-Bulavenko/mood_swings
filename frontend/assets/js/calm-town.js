// ====== BREATHE OVERLAY ======
const breatheOverlay = document.getElementById("breatheOverlay");
const breatheStartBtn = document.getElementById("breatheStartBtn");
const breatheCloseBtn = document.getElementById("breatheCloseBtn");
const breatheCircle = document.querySelector(".breatheCircle");
const breatheStatus = document.getElementById("breatheStatus");

function openBreatheOverlay() {
  if (breatheOverlay) breatheOverlay.hidden = false;
}

function closeBreatheOverlay() {
  if (breatheOverlay) breatheOverlay.hidden = true;
  stopBreathing();
}

let breatheIntervalId = null;

function startBreathing() {
  if (!breatheCircle) return;

  if (breatheIntervalId) {
    clearTimeout(breatheIntervalId);
    breatheIntervalId = null;
  }

  breatheCircle.classList.add("isBreathing");
  if (breatheStatus) breatheStatus.textContent = "Let's begin. Inhale…";

  const phases = [
    { text: "Inhale…", duration: 4000 },
    { text: "Hold…", duration: 3000 },
    { text: "Exhale…", duration: 5000 },
    { text: "Hold…", duration: 3000 },
  ];

  let phaseIndex = 0;

  function showPhase() {
    if (breatheStatus) breatheStatus.textContent = phases[phaseIndex].text;
    const nextDuration = phases[phaseIndex].duration;
    phaseIndex = (phaseIndex + 1) % phases.length;
    breatheIntervalId = setTimeout(showPhase, nextDuration);
  }

  showPhase();
}

function stopBreathing() {
  if (breatheCircle) breatheCircle.classList.remove("isBreathing");
  if (breatheIntervalId) {
    clearTimeout(breatheIntervalId);
    breatheIntervalId = null;
  }
  if (breatheStatus) breatheStatus.textContent = "Ready when you are.";
}

// Button wiring
if (breatheStartBtn) breatheStartBtn.addEventListener("click", startBreathing);
if (breatheCloseBtn) breatheCloseBtn.addEventListener("click", closeBreatheOverlay);
const pageBreatheBtn = document.getElementById("pageBreatheBtn");
if (pageBreatheBtn) pageBreatheBtn.addEventListener("click", openBreatheOverlay);


// ====== VIDEO OVERLAYS ======
const headspaceOverlay = document.getElementById("headspaceOverlay");
const headspaceCloseBtn = document.getElementById("headspaceCloseBtn");
const headspaceVideo = document.getElementById("headspaceVideo");
const headspaceBtn = document.getElementById("headspaceBtn");

const adrieneOverlay = document.getElementById("adrieneOverlay");
const adrieneCloseBtn = document.getElementById("adrieneCloseBtn");
const adrieneVideo = document.getElementById("adrieneVideo");
const adrieneBtn = document.getElementById("adrieneBtn");

const musicOverlay = document.getElementById("musicOverlay");
const musicCloseBtn = document.getElementById("musicCloseBtn");
const musicVideo = document.getElementById("musicVideo");
const musicBtn = document.getElementById("musicBtn");

function openHeadspace() {
    document.getElementById("headspaceSpinner").style.display = "block";
    document.getElementById("headspaceVideo").style.display = "none";
    headspaceVideo.src = "https://www.youtube.com/embed/inpok4MKVLM?autoplay=1";
    headspaceVideo.setAttribute("allow", "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share");
    headspaceVideo.setAttribute("referrerpolicy", "strict-origin-when-cross-origin");
    headspaceOverlay.hidden = false;
    headspaceVideo.onload = function() {
        document.getElementById("headspaceSpinner").style.display = "none";
        document.getElementById("headspaceVideo").style.display = "block";
    };
}

function closeHeadspace() {
    headspaceVideo.src = "";
    headspaceOverlay.hidden = true;
}


function openAdriene() {
    document.getElementById("adrieneSpinner").style.display = "block";
    document.getElementById("adrieneVideo").style.display = "none";
    adrieneVideo.src = "https://www.youtube.com/embed/ZiQh8jA5tVM?si=pJA-7xeKPX0fHBzR&autoplay=1";
    adrieneVideo.setAttribute("allow", "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share");
    adrieneVideo.setAttribute("referrerpolicy", "strict-origin-when-cross-origin");
    adrieneOverlay.hidden = false;
    adrieneVideo.onload = function() {
        document.getElementById("adrieneSpinner").style.display = "none";
        document.getElementById("adrieneVideo").style.display = "block";
    };
}

function closeAdriene() {
    adrieneVideo.src = "";
    adrieneOverlay.hidden = true;
}

if (headspaceBtn) headspaceBtn.addEventListener("click", openHeadspace);
if (headspaceCloseBtn) headspaceCloseBtn.addEventListener("click", closeHeadspace);
if (adrieneBtn) adrieneBtn.addEventListener("click", openAdriene);
if (adrieneCloseBtn) adrieneCloseBtn.addEventListener("click", closeAdriene);


function openMusic() {
    document.getElementById("musicSpinner").style.display = "block";
    document.getElementById("musicVideo").style.display = "none";
    musicVideo.src = "https://www.youtube.com/embed/dnBAU8Co6PA?si=vaEUO0nEcnpxm_fl&autoplay=1";
    musicVideo.setAttribute("allow", "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share");
    musicVideo.setAttribute("referrerpolicy", "strict-origin-when-cross-origin");
    musicOverlay.hidden = false;
    musicVideo.onload = function() {
        document.getElementById("musicSpinner").style.display = "none";
        document.getElementById("musicVideo").style.display = "block";
    };
}


function closeMusic() {
    musicVideo.src = "";
    musicOverlay.hidden = true;
}

if (musicBtn) musicBtn.addEventListener("click", openMusic);
if (musicCloseBtn) musicCloseBtn.addEventListener("click", closeMusic);

// ====== WORD CLOUD OVERLAY ======
const wordCloudOverlay = document.getElementById("wordCloudOverlay");
const wordCloudBtn = document.getElementById("wordCloudBtn");
const wordCloudCloseBtn = document.getElementById("wordCloudCloseBtn");

function openWordCloud() {
    wordCloudOverlay.hidden = false;
}

function closeWordCloud() {
    wordCloudOverlay.hidden = true;
}

if (wordCloudBtn) wordCloudBtn.addEventListener("click", openWordCloud);
if (wordCloudCloseBtn) wordCloudCloseBtn.addEventListener("click", closeWordCloud);