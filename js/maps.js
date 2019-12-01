// Show Map Functions

const showMap = async (arr,target,callback) => {
    await checkData(()=>window.google);

	const tm = $(target);
	const sf = {lat:37.786269, lng:-122.399321};

	if(!tm.data("map")) {
	    tm.data(
	    	"map",
	    	new google.maps.Map(tm[0], {
		        center: sf,
		        zoom: 11,
		        disableDefaultUI: true,
		        styles:mapStyles
		    })
	    )
	    .data(
	    	"infoWindow",
	    	new google.maps.InfoWindow({
	    		content:''
		    })
	    );
	}

	if(tm.data("markers")) {
		tm.data("markers").forEach(o=>o.setMap(null));
	}

	tm.data("markers",[]);

	arr.forEach(o=>{
	    let marker = new google.maps.Marker({
			position:o,
			map: tm.data("map"),
			icon:{
				url:o.icon,
				scaledSize: {
					width:40,
					height:40
				}
			}
		});
		tm.data("markers").push(marker);
	});

	if(callback) callback(target);
}


let mapStyles = [
    {
        "featureType": "administrative",
        "elementType": "all",
        "stylers": [
            {
                "hue": "#ff0000"
            }
        ]
    },
    {
        "featureType": "landscape",
        "elementType": "geometry.fill",
        "stylers": [
            {
                "weight": "1"
            },
            {
                "color": "#e2e0dd"
            },
            {
                "saturation": "0"
            }
        ]
    },
    {
        "featureType": "landscape.natural.landcover",
        "elementType": "geometry.fill",
        "stylers": [
            {
                "saturation": "100"
            },
            {
                "lightness": "49"
            }
        ]
    },
    {
        "featureType": "poi.park",
        "elementType": "geometry.fill",
        "stylers": [
            {
                "color": "#c2d0a6"
            }
        ]
    },
    {
        "featureType": "road",
        "elementType": "geometry.fill",
        "stylers": [
            {
                "color": "#b2b2b2"
            }
        ]
    },
    {
        "featureType": "water",
        "elementType": "geometry.fill",
        "stylers": [
            {
                "color": "#80aaa6"
            }
        ]
    }
];