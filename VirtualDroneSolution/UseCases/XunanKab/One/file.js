function initMap() {

  var uluru = {lat: 20.654544, lng: -103.3930971}; 

  var locations = [
      ['Drone One', 20.654544, -103.3930971, 4],
      ['Drone Two', 20.654444, -103.3930071, 5],
      ['Drone Three', 20.654344, -103.3930171, 3],
      ['Drone Four', 20.654244, -103.3930271, 2],
      ['Drone Five', 20.654144, -103.3930371, 1]
    ];
    
  var map = new google.maps.Map(document.getElementById('map'), { 
			zoom: 4,
      center: uluru
  }); 

  var marker, i;

  for (i = 0; i < locations.length; i++) {  
    marker = new google.maps.Marker({
      position: new google.maps.LatLng(locations[i][1], locations[i][2]),
      map: map
    });

    google.maps.event.addListener(marker, 'click', (function(marker, i) {
      return function() {
        infowindow.setContent(locations[i][0]);
        infowindow.open(map, marker);
      }
    })(marker, i));
  }
}
