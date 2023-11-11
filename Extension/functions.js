export function getCurrentURL(callback) {
  chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
    if (tabs.length > 0) {
      const url = tabs[0].url;
      callback(url);
    }
  });
}
