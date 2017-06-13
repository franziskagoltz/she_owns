// ES6 class generating a map centered in SF
// TODO: add a selectCategory function to class that set markers based on passed objects from DB

class showMap {
    constructor() {
      this.initMap();
    }
    initMap() {
        const map = new google.maps.Map(document.getElementById("map"), {
          center: {lat: 37.7749, lng: -122.4194},
          zoom: 10
        });
      }
}

export default showMap;

