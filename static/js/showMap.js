// ES6 class generating a map centered in SF
import fetch from "isomorphic-fetch";


class showMap {
    constructor() {
      this.gMarkers = [];
      this.map;
      this.initMap();

    }
    initMap() {
        this.map = new google.maps.Map(document.getElementById("map"), {
          // center map on SF
          center: {lat: 37.7749, lng: -122.4194},
          zoom: 12
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
                      var marker = new google.maps.Marker({
                          map: this.map,
                          position: newMarker,
                          title: business.name
                        });

                      this.gMarkers.push(marker);

                      var contentString = "<h4><a href='/businesses/"
                                          +business.business_id+"'>"
                                          +business.name+"</a></h4>"
                                          +"<p>"+business.address+"</p>";

                      var infowindow = new google.maps.InfoWindow({
                        content: contentString
                      });

                      marker.addListener('click', function() {
                        infowindow.open(map, marker);
                      });

                    })

      }
      deleteMarkers() {

          for(var i=0; i<this.gMarkers.length; i++){
            this.gMarkers[i].setMap(null);
          }
      }

}

export default showMap;
