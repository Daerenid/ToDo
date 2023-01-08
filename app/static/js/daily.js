function pass() {
  var checkbox = document.getElementById("checkbox");
  var desc = document.getElementById("description");
  console.log("elo");

  if (checkbox.checked == True) {
    console.log("elo2");
    desc.style.textDecoration = "line-through";
    desc.style.color = "red";
  } else {
    desc.style.textDecoration = "none";
  }
}
