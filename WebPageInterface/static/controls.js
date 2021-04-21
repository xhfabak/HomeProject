function changeMode(mode, elementId){
// FIX ME to check the response before performing any actions
       var xhttp = new XMLHttpRequest();
       xhttp.open("POST", `http://127.0.0.1:5000/rekuperatorius?mode=${mode}`, true);
       xhttp.setRequestHeader("Access-Control-Allow-Origin", "true");
       xhttp.send();

       var currentActiveModeElements = document.getElementsByClassName("mode-container active-mode");
       if (currentActiveModeElements.length > 0) {
          currentActiveModeElements[0].classList.remove("active-mode");
       }
       document.getElementById(elementId).classList.add("active-mode");
    }
async function getRefreshData() {
 console.log("Hitted");
   // const userAction = async () => {
    const response = await fetch('http://127.0.0.1/rekuperatorius');
    const myJson = await response.json(); //extract JSON from the http response
    console.log(myJson);
  // do something with myJson
    // }
   // console.log(userAction);
}