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

function openHeadspace() {
    headspaceVideo.src = "https://www.youtube.com/embed/inpok4MKVLM?autoplay=1";
    headspaceOverlay.hidden = false;
}

function closeHeadspace() {
    headspaceVideo.src = "";
    headspaceOverlay.hidden = true;
}

function openAdriene() {
    adrieneVideo.src = "https://www.youtube.com/embed/ZiQh8jA5tVM?si=pJA-7xeKPX0fHBzR&autoplay=1";
    adrieneVideo.setAttribute("allow", "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share");
    adrieneVideo.setAttribute("referrerpolicy", "strict-origin-when-cross-origin");
    adrieneOverlay.hidden = false;
}

function closeAdriene() {
    adrieneVideo.src = "";
    adrieneOverlay.hidden = true;
}

if (headspaceBtn) headspaceBtn.addEventListener("click", openHeadspace);
if (headspaceCloseBtn) headspaceCloseBtn.addEventListener("click", closeHeadspace);
if (adrieneBtn) adrieneBtn.addEventListener("click", openAdriene);
if (adrieneCloseBtn) adrieneCloseBtn.addEventListener("click", closeAdriene);