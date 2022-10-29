//NOT GOOD AT JAVASCRIPT CAN USE BETTER CONTDITIONS

addEventListener("DOMContentLoaded", (event) => {
  hideAllRelatedStuff("choose_image");
  hideAllRelatedStuff("choose_sound");
  hideAllRelatedStuff("choose_video");
  let select = document.getElementById("opt");
  select.addEventListener("change", (e) => {
    if (select.value === "camera") {
      hideAllRelatedStuff("choose_image");
      hideAllRelatedStuff("choose_sound");
      hideAllRelatedStuff("choose_video");
    } else if (select.value === "image") {
      showAllRelatedStuff("choose_image");
      hideAllRelatedStuff("choose_sound");
      hideAllRelatedStuff("choose_video");
    } else if (select.value === "sound") {
      hideAllRelatedStuff("choose_image");
      showAllRelatedStuff("choose_sound");
      hideAllRelatedStuff("choose_video");
    } else {
      hideAllRelatedStuff("choose_image");
      hideAllRelatedStuff("choose_sound");
      showAllRelatedStuff("choose_video");
    }
  });
});

function hideAllRelatedStuff(elementId) {
  let chooser = document.getElementById(elementId);
  chooser.style.display = "none";
  for (const label of chooser.labels) {
    label.style.display = "none";
  }
}

function showAllRelatedStuff(elementId) {
  let chooser = document.getElementById(elementId);
  chooser.style.display = "";
  for (const label of chooser.labels) {
    label.style.display = "";
  }
}

function handle_stop_click() {
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "http://127.0.0.1:5000/stop", true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send();
  return false;
}
