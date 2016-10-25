function clearStatus() {
  var target = document.getElementById("placeholder");
  target.innerHTML = "No one here"
}

function listen() {
  var source = new EventSource("/stream/");
  var target = document.getElementById("placeholder");
  source.onmessage = function(msg) {
    target.innerHTML = msg.data + '<br>';
    setTimeout(clearStatus, 5000)
    if (msg.data == "here") {
      alert("Some one is here")
    }
  }
}
listen();
