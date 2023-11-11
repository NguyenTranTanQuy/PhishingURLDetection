import { getCurrentURL } from "./functions.js";

getCurrentURL(function (url_) {
  fetch("http://127.0.0.1:5000/api/data", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      url: url_,
    }),
  })
    .then((response) => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error("Network response was not ok");
      }
    })
    .then((data) => {
      // Display the data on the web page
      const labelData = document.querySelector("#label>b");
      const probabilityData = document.querySelector("#probability>b");

      labelData.textContent = data.messenger;

      if (data.messenger == "Phishing" || data.messenger == "Legitimate") {
        if (data.messenger == "Phishing") labelData.style.color = "red";
        else labelData.style.color = "green";
      }

      probabilityData.textContent = data.probability;
    })
    .catch((error) => {
      console.error("There was a problem with the fetch operation:", error);
    });
});
