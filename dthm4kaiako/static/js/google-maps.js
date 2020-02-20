window.initMap = function() {
    var map_markers = [];
    var infowindow = new google.maps.InfoWindow();
    if (event_markers.length == 1) {
        var center_lat_lng = event_markers[0].coords;
    } else {
        var center_lat_lng = { lat: -41, lng: 174 };
    }
    var map_zoom = window.map_zoom || 5;
    var map = new google.maps.Map(
        document.getElementById('map'),
        {
            zoom: map_zoom,
            center: center_lat_lng,
        }
    );

    function addMarker(location) {
        var marker = new google.maps.Marker({
            position: location.coords,
            map: map,
            title: location.title,
        });
        map_markers.push(marker);

        marker.addListener('click', function () {
            // Close previously opened infowindow
            infowindow.close();
            infowindow.setContent(location.text);
            infowindow.open(map, marker);
        });
    }

    for (var i = 0; i < event_markers.length; i++) {
        addMarker(event_markers[i]);
    }

    if (event_markers.length > 1) {
        var markerCluster = new MarkerClusterer(map, map_markers,
            { imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m' });
    }
}
