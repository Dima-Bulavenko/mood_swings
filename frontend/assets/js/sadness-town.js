// ====== FUNNY VIDEO OVERLAY ======
const funnyOverlay = document.getElementById("funnyOverlay");
const funnyCloseBtn = document.getElementById("funnyCloseBtn");
const funnyVideo = document.getElementById("funnyVideo");
const funnyBtn = document.getElementById("funnyBtn");

function openFunny() {
    document.getElementById("funnySpinner").style.display = "block";
    document.getElementById("funnyVideo").style.display = "none";
    funnyVideo.src = "https://www.youtube.com/embed/CJkrxF6DiJs?si=o-gfnOTTO5SchQ9x&autoplay=1";
    funnyVideo.setAttribute("allow", "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share");
    funnyVideo.setAttribute("referrerpolicy", "strict-origin-when-cross-origin");
    funnyOverlay.hidden = false;
    funnyVideo.onload = function() {
        document.getElementById("funnySpinner").style.display = "none";
        document.getElementById("funnyVideo").style.display = "block";
    };
}

function closeFunny() {
    funnyVideo.src = "";
    funnyOverlay.hidden = true;
}

if (funnyBtn) funnyBtn.addEventListener("click", openFunny);
if (funnyCloseBtn) funnyCloseBtn.addEventListener("click", closeFunny);

// ====== MUSIC OVERLAY ======
const sadMusicOverlay = document.getElementById("sadMusicOverlay");
const sadMusicCloseBtn = document.getElementById("sadMusicCloseBtn");
const sadMusicBtn = document.getElementById("sadMusicBtn");

function openSadMusic() {
    sadMusicOverlay.hidden = false;
}

function closeSadMusic() {
    sadMusicOverlay.hidden = true;
}

if (sadMusicBtn) sadMusicBtn.addEventListener("click", openSadMusic);
if (sadMusicCloseBtn) sadMusicCloseBtn.addEventListener("click", closeSadMusic);

// ====== POETRY OVERLAY ======
const poetryOverlay = document.getElementById("poetryOverlay");
const poetryCloseBtn = document.getElementById("poetryCloseBtn");
const poetryBtn = document.getElementById("poetryBtn");

function openPoetry() {
    poetryOverlay.hidden = false;
}

function closePoetry() {
    poetryOverlay.hidden = true;
}

if (poetryBtn) poetryBtn.addEventListener("click", openPoetry);
if (poetryCloseBtn) poetryCloseBtn.addEventListener("click", closePoetry);

// ====== WORD CLOUD OVERLAY ======
const sadWordCloudOverlay = document.getElementById("sadWordCloudOverlay");
const sadWordCloudBtn = document.getElementById("sadWordCloudBtn");
const sadWordCloudCloseBtn = document.getElementById("sadWordCloudCloseBtn");

function openSadWordCloud() {
    sadWordCloudOverlay.hidden = false;
}

function closeSadWordCloud() {
    sadWordCloudOverlay.hidden = true;
}

if (sadWordCloudBtn) sadWordCloudBtn.addEventListener("click", openSadWordCloud);
if (sadWordCloudCloseBtn) sadWordCloudCloseBtn.addEventListener("click", closeSadWordCloud);