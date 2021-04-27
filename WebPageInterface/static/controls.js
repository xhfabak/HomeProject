var modeMapping =
{
    1: "away-image",
    2: "normal-image",
    3: "intensive-image",
    4: "boost-image",
};

function changeMode(mode){
       const thisId = modeMapping[mode];
       fetch(new Request(`http://127.0.0.1:5000/rekuperatorius?mode=${mode}`,
         {
             method: "POST",
             headers: {"Access-Control-Allow-Origin": "true"}
         }
       )).then(response => {
           if (!response.ok) throw Error(response.statusText)
           coloring(thisId);
           return response;
        }).catch(error => console.log(error));
}

function coloring(elementId){

           const currentActiveModeElements = document.getElementsByClassName("mode-desc active-mode");
           if (currentActiveModeElements.length > 0) {
              currentActiveModeElements[0].classList.remove("active-mode");
           }
           document.getElementById(elementId).classList.add("active-mode");
}

function loadedDataDa() {
    const fetchPromise = fetch("http://127.0.0.1:5000/rekuperatorius/data");
    fetchPromise.then(response => {
    return response.json();
    }).then(test => {
        document.getElementById("current-humidity").innerHTML = test.humidity;
        document.getElementById("current-supply").innerHTML = test.supply;
        document.getElementById("current-filter").innerHTML = test.filter;
        document.getElementById("current-eco").innerHTML = test.eco;
        document.getElementById("current-heater").innerHTML = test.heater;
        let mode = test.curr_mode;
        let elementId = modeMapping[mode];
        coloring(elementId);
    });
    }

function loadControls()
{
    loadedDataDa();
    setInterval(loadedDataDa, 3000);  // Time is ms
}
