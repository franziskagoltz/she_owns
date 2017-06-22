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



