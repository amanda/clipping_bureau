function getClip() {
  if (typeof window.getSelection() !== "undefined") {
    var selection = window.getSelection();
    if (selection.rangeCount) {
      //get copied text and save in variable
      var newClip = selection.toString();
      //copied text -> server
      var clipperRequest = new XMLHttpRequest();
      var url = 'http://127.0.0.1:5000/add_from_web?content=' + newClip; //local
      clipperRequest.open("POST", url, true);
      clipperRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
      clipperRequest.send();
    }
  }
}
