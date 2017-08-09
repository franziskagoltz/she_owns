// single map for business details page

class SingleMap {

    constructor() {
        this.singleMap;
        this.initSingleMap();
    }

    initSingleMap() {
        this.singleMap = new google.maps.Map(document.getElementById("single_map"), {
          // center map on business location
          center: latlng,
          zoom: 16
        });
    }

    addMarker() {
      // create and set a marker and specific location
      var marker = new google.maps.Marker({
          map: this.singleMap,
          position: latlng,
        });
    }

}

export default SingleMap;