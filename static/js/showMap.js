// ES6 class generating a map centered in SF
// TODO: add a selectCategory function to class that set markers based on passed objects from DB
import fetch from "isomorphic-fetch";


class showMap {
    constructor() {
      this.initMap();
    }
    initMap() {
        const map = new google.maps.Map(document.getElementById("map"), {
          // center map on SF
          center: {lat: 37.7749, lng: -122.4194},
          zoom: 11
        });

        // placeholder address of Trouble Coffee Shop in San Francisco
        var address = "4033 Judah St, San Francisco, CA 94122";

        // making API call to geocode address into lat/lng to create markers
        fetch("https://maps.googleapis.com/maps/api/geocode/json?address="+
              address+"&key=AIzaSyA_v4tGjA9aTrB5HL7ZZs5Df7I5h7k31uY").then(
                (response) => {
                    return response.json() }).then( (results) => {

                      // getting lat/lng of address passed to API
                      var newMarker = results.results[0].geometry.location

                      // create and set a marker and specific location
                      new google.maps.Marker({
                          map: map,
                          position: newMarker,
                          title: 'Hi Business!'
                        });
                    })
      }
}

export default showMap;

