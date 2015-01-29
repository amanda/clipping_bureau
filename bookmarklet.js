function getClip() {
  if (typeof window.getSelection() !== "undefined") {
    var selection = window.getSelection();
    if (selection.rangeCount) {
      var newClip = encodeURIComponent(selection);
      var clipperRequest = new XMLHttpRequest();
      var url = 'http://127.0.0.1:5000/add_from_web?content=' + newClip;
      clipperRequest.open("POST", url, true);
      clipperRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
      clipperRequest.send();
      alert('saved clip!');
    }
  }
}
