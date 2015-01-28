function getClip() {
  if (typeof window.getSelection() !== "undefined") {
    var selection = window.getSelection();
    if (selection.rangeCount) {
      var newClip = selection;
      console.log(newClip);
      var clipperRequest = new XMLHttpRequest();
      var url = 'http://127.0.0.1:5000/add_from_web'; //running locally for now
      var data = 'content=' + newClip;
      console.log(data);
      clipperRequest.open("POST", url, true);
      clipperRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
      clipperRequest.send(data);
    }
  }
}
