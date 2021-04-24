function changeMode(mode, elementId){
         fetch(new Request(`http://127.0.0.1:5000/rekuperatorius?mode=${mode}`,
         {
             method: "POST",
             headers: {"Access-Control-Allow-Origin": "true"}
         }
       )).then(response => {
           if (!response.ok) throw Error(response.statusText)
           const currentActiveModeElements = document.getElementsByClassName("mode-desc active-mode");
           if (currentActiveModeElements.length > 0) {
              currentActiveModeElements[0].classList.remove("active-mode");
           }
           document.getElementById(elementId).classList.add("active-mode");
           return response;
        }).catch(error => console.log(error));
}

async function getRefreshData() {
    fetch(new Request('http://127.0.0.1:5000/rekuperatorius/data'), { method: "GET",
                                                                      headers: {"Access-Control-Allow-Origin": "true"}})
      .then(response => {
      console.log(response);
      const data = response.json
      console.log(data);
       //sorted_data(data)
    }).catch(error => console.log(error));
//    const myJson = await response.json(); //extract JSON from the http response
//    console.log(myJson);
}

//function sorted_data(loaded_rek_data) {
////  document.getElementById("current-humidity").innerHTML = loaded_rek_data.A.AH;  // AH - Humidity data (int + symbol + str)
////  document.getElementById("current-filter").innerHTML = loaded_rek_data.A.FCG;   // FCG - Filter data (int + str)
////  document.getElementById("current-supply").innerHTML = loaded_rek_data.A.AI0;   // AI0 - Supply temperature (int + symbol + str)
////  document.getElementById("current-eco").innerHTML = loaded_rek_data.A.VF;       // VF -  Eco mode (int)
////  document.getElementById("current-heater").innerHTML = loaded_rek_data.A.EC4;   // EC4 - Current Heater W. usage (int + str)
//
//  setInterval(function(){
//                         console.log('Tested');
//                         return sorted_data()
//                        }, 5000)
//                                        }