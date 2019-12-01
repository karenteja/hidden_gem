// Show Page Functions

const showListPage = async () => {
    await checkData(()=>db.length);

    console.log("List Page",db);
    $("#bars-list .bars-list")
        .html(makeBarsList(currentUser().bars))
}




const showMapPage = async () => {
    // if(!waitForDB(showMapPage)) return false;
    await checkData(()=>db.length);

    let locs = currentUser().bars.reduce((r,o)=>{
        if(o.locations.length) {
            let last = o.locations.slice(-1)[0];
            last.icon = o.img;
            last.barId = o.id;
            r.push(last);
        }
        return r;
    },[])

    showMap(
        locs,
        "#page-map .map",
        t=>{
            console.log(t);
            let tm = $(t);

            tm.data("markers").forEach((o,i)=>{

                let bar = getBar(
                    currentUser(),
                    locs[i].barId);

                o.addListener("click",e=>{
                    // console.log(e);

                    tm.data("infoWindow")
                        // ${locs[i].lat} x ${locs[i].lng}<br>

                        .setContent(`
                        <div class="flex-parent bar-jump" data-id="${bar.id}">
                        <div class="noclick">
                            <img src="${bar.img}" style="width:75px">
                        </div>
                        <div class="noclick" style="padding-left:1em">
                            <strong>${bar.bar_name}</strong><br>
                            <strong>Area</strong> ${bar.area}<br>
                            <strong>Locations</strong> ${bar.locations.length}
                        </div>
                        </div>
                        `);

                    tm.data("infoWindow")
                        .open(tm[0],o);

                    // $("#page-map .menu").addClass("active")
                })
            })
        }
    );
}




const showBarProfilePage = async () => {
    await checkData(()=>db.length);

    $("#page-bar-profile .bar-profile-top")
        .html(makeBarProfile(currentBar()));

    showMap(
        currentBar().locations.map(o=>{
            o.icon = currentBar().img;
            return o;
        }),
        "#page-bar-profile .map",
        t=>{
            console.log(t);
            let tm = $(t);

            tm.data("map").addListener("click",e=>{
                console.log(e.latLng.lat(),e.latLng.lng());
                console.log("center of map",tm.data("map").getCenter())

                $("#add-location-lat").val(e.latLng.lat());
                $("#add-location-lng").val(e.latLng.lng());
                $("#add-location-modal").addClass("active");
            })

        }
    );
}




const showUserProfilePage = async () => {
    await checkData(()=>db.length);

    $(".user-profile")
        .html(makeUserProfile(currentUser()))
}
