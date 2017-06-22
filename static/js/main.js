//import searchTerm from "./getBusinesses";
import $ from "jquery";
import fetch from "isomorphic-fetch";
import showMap from "./showMap";


// instantiating jsMap object
let jsMap;
function initMap() {
    jsMap = new showMap();
}

// setting initmap global, so googlemaps api link can access callback
window.initMap = initMap


// click event searching for categories
$("#find").on("click", () => {

    let searchTerm = $("#search").val();

    // call to json route to get data
    fetch("/getBusinessInfo.json"+"?searchTerm="+searchTerm).then( (response) => {

        return response.json()
    }).then( (value) => {

         return value[0]

    }).then ( (businesses) => {
        try {
            businesses.forEach( (business) => {

              // add marker to for ever business returned
              jsMap.addMarker(business)

            });
        }

        // handing error when no results were returned - todo: handle error
        catch(TypeError) {
            console.log(TypeError);
        }
    })

})

