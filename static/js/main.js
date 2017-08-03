//import searchTerm from "./getBusinesses";
import $ from "jquery";
import fetch from "isomorphic-fetch";
import showMap from "./showMap";
import SingleMap from "./single-map";


let singleMap;
function initSingleMap() {
    singleMap = new SingleMap();
    singleMap.addMarker();
}

// setting initSingleMap global, so googlemaps api link can access callback
window.initSingleMap = initSingleMap


// instantiating jsMap object
let jsMap;
function initMap() {
    jsMap = new showMap();
}

// setting initmap global, so googlemaps api link can access callback
window.initMap = initMap


// click event searching for categories
$("#find").on("click", (evt) => {
evt.preventDefault();

    let searchTerm = $("#search").val();

    // delete old markers and then empty the array of markers from old search
    // results, based on https://developers.google.com/maps/documentation/
    //                   javascript/examples/marker-remove
    jsMap.deleteMarkers();
    jsMap.gMarkers = [];

    // call to json route to get data
    fetch("/getBusinessInfo.json"+"?searchTerm="+searchTerm).then( (response) => {

        return response.json()
    }).then( (value) => {

         // value[0] is the list of businesses
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

