chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === "READ_PAGE_CONTENT") {
    sendResponse({
      url: window.location.href,
      content: document.body.innerText
    });
  }
});
