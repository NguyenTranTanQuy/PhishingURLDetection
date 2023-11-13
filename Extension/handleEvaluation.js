import { getCurrentURL } from "./functions.js";

const noButton = document.getElementById("no");
const yesButton = document.getElementById("yes");

getCurrentURL(function (url_) {
  const evaluation = document.getElementById("evaluate");
  noButton.addEventListener("click", function () {
    // Make a POST request to the server
    fetch("http://localhost:5000/api/evaluatedData", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        url: url_,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
    evaluation.textContent = "Thanks for your feedback!";
    evaluation.style.alignSelf = "center";
    evaluation.style.padding = "8px 16px";
    evaluation.style.border = "1px solid #333";
    evaluation.style.marginTop = "8px";
    evaluation.style.borderRadius = "12px";
    evaluation.style.backgroundColor = "green";
    evaluation.style.color = "#fff";
  });

  yesButton.addEventListener("click", function () {
    evaluation.textContent = "Thanks for your feedback!";
    evaluation.style.alignSelf = "center";
    evaluation.style.padding = "8px 16px";
    evaluation.style.border = "1px solid #333";
    evaluation.style.marginTop = "8px";
    evaluation.style.borderRadius = "12px";
    evaluation.style.backgroundColor = "green";
    evaluation.style.color = "#fff";
  });
});
