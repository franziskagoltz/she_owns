// ES6 class generating a map centered in SF
import fetch from "isomorphic-fetch";


let map;
class showMap {
    constructor() {
      this.initMap();
    }
    initMap() {
        map = new google.maps.Map(document.getElementById("map"), {
          // center map on SF
          center: {lat: 37.7749, lng: -122.4194},
          zoom: 11
        });
    }
    addMarker(business) {

        // making API call to geocode address into lat/lng to create markers
        // placeholder for now -- will add lat/lng to db & make api call when
        // populating the database
        fetch("https://maps.googleapis.com/maps/api/geocode/json?address="+
              business.address+"&key="+gMapsKey).then(
                (response) => {
                    return response.json() }).then( (results) => {

                      // getting lat/lng of address passed to API
                      var newMarker = results.results[0].geometry.location

                      // create and set a marker and specific location
                      new google.maps.Marker({
                          map: map,
                          position: newMarker,
                          title: business.name
                        });
                    })
      }
}

export default showMap;

