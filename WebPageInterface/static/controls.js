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
    fetch(new Request('http://127.0.0.1:5000/rekuperatorius/data'), { method: "GET", headers: {"Access-Control-Allow-Origin": "true"}})
      .then(response => {
       reused_trusai(response)
    }).catch(error => console.log(error));
//    const myJson = await response.json(); //extract JSON from the http response
  //  console.log(myJson);
}

// OMO - Rekuperatorius mode name
// AH - Humidity data
// FCG - FIlter data
// AI0 - Supplpy temperature
function reused_trusai(rekup_data) {
  document.getElementById("current-humidity").value = rekup_data.A.AH;
}


//return an array of values that match on a certain key
function getValues(obj, key) {
    var objects = [];
    for (var i in obj) {
        if (!obj.hasOwnProperty(i)) continue;
        if (typeof obj[i] == 'object') {
            objects = objects.concat(getValues(obj[i], key));
        } else if (i == key) {
            objects.push(obj[i]);
        }
    }
    return objects;
}

//return an array of keys that match on a certain value
function getKeys(obj, val) {
    var objects = [];
    for (var i in obj) {
        if (!obj.hasOwnProperty(i)) continue;
        if (typeof obj[i] == 'object') {
            objects = objects.concat(getKeys(obj[i], val));
        } else if (obj[i] == val) {
            objects.push(i);
        }
    }
    return objects;
}