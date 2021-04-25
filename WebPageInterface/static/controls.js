function changeMode(mode, elementId){
         fetch(new Request(`http://127.0.0.1:5000/rekuperatorius?mode=${mode}`,
         {
             method: "POST",
             headers: {"Access-Control-Allow-Origin": "true"}
         }
       )).then(response => {
           if (!response.ok) throw Error(response.statusText)
           coloring(elementId);
//           const currentActiveModeElements = document.getElementsByClassName("mode-desc active-mode");
//           if (currentActiveModeElements.length > 0) {
//              currentActiveModeElements[0].classList.remove("active-mode");
//           }
//           document.getElementById(elementId).classList.add("active-mode");

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

const loadedDataDa = () => {
    const fetchPromise = fetch("http://127.0.0.1:5000/rekuperatorius/data");
    fetchPromise.then(response => {
    return response.json();
    }).then(test => {document.getElementById("current-humidity").innerHTML = test.humidity;
                     document.getElementById("current-supply").innerHTML = test.supply;
                     document.getElementById("current-filter").innerHTML = test.filter;
                     document.getElementById("current-eco").innerHTML = test.eco;
                     document.getElementById("current-heater").innerHTML = test.heater;
                     // Add return of current mode with solved JS file
    });
    }

setInterval(function() {loadedDataDa();}, 3000)  // Time is ms