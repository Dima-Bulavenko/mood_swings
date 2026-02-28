(function () {
  function isBlankSrc(src) {
    if (!src) {
      return true;
    }

    return src.trim().toLowerCase() === 'about:blank';
  }

  function isYouTubeEmbed(url) {
    return /youtube(?:-nocookie)?\.com\/embed/i.test(url || '');
  }

  function restoreIframeSource(iframe) {
    const storedSource = iframe.dataset.src;

    if (!storedSource) {
      return;
    }

    const currentSource = iframe.getAttribute('src') || '';
    if (isBlankSrc(currentSource)) {
      iframe.setAttribute('src', storedSource);
    }
  }

  function stopYouTubeIframe(iframe) {
    const source = iframe.dataset.src || iframe.getAttribute('src') || '';

    if (!isYouTubeEmbed(source) || !iframe.contentWindow) {
      return;
    }

    iframe.contentWindow.postMessage('{"event":"command","func":"pauseVideo","args":""}', '*');
    iframe.contentWindow.postMessage('{"event":"command","func":"stopVideo","args":""}', '*');
  }

  function stopHtmlMediaElement(mediaElement) {
    if (mediaElement.dataset.originalMuted === undefined) {
      mediaElement.dataset.originalMuted = String(mediaElement.muted);
    }

    mediaElement.pause();
    mediaElement.muted = true;

    if (typeof mediaElement.currentTime === 'number') {
      try {
        mediaElement.currentTime = 0;
      } catch (error) {
        return;
      }
    }
  }

  function restoreHtmlMediaElement(mediaElement) {
    if (mediaElement.dataset.originalMuted !== undefined) {
      mediaElement.muted = mediaElement.dataset.originalMuted === 'true';
    }
  }

  function bindModalMedia(modalElement) {
    if (modalElement.dataset.modalMediaBound === 'true') {
      return;
    }

    modalElement.dataset.modalMediaBound = 'true';

    modalElement.querySelectorAll('iframe').forEach(function (iframe) {
      const currentSource = iframe.getAttribute('src') || '';

      if (!iframe.dataset.src && !isBlankSrc(currentSource)) {
        iframe.dataset.src = currentSource;
        iframe.setAttribute('src', 'about:blank');
      }
    });

    modalElement.addEventListener('show.bs.modal', function () {
      modalElement.querySelectorAll('iframe[data-src]').forEach(restoreIframeSource);
      modalElement.querySelectorAll('audio, video').forEach(restoreHtmlMediaElement);
    });

    modalElement.addEventListener('hidden.bs.modal', function () {
      modalElement.querySelectorAll('iframe').forEach(function (iframe) {
        stopYouTubeIframe(iframe);
        iframe.setAttribute('src', 'about:blank');
      });

      modalElement.querySelectorAll('audio, video').forEach(stopHtmlMediaElement);
    });
  }

  function initModalMedia(root) {
    (root || document).querySelectorAll('.modal').forEach(bindModalMedia);
  }

  window.MoodSwingsModalMedia = {
    init: initModalMedia,
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      initModalMedia(document);
    });
    return;
  }

  initModalMedia(document);
})();
