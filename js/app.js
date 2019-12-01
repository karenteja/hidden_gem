let db = [];








$.ajax({
	url:'data/data.json',
	dataType:'json'
})
.done(d=>{
	db = d;
})




// Document Ready
$(()=>{

	checkStorage();

	// Delegate Events
	$(document)

	.on("pagecontainerbeforeshow",(e,ui)=>{
		console.log(e, ui, ui.toPage[0].id);

		switch(ui.toPage[0].id) {
			case "page-map":
				// run some code
				showMapPage();
				break;
			case "bars-list":
				showListPage();
				break;
			case "page-bar-profile":
				showBarProfilePage();
				break;
			case "page-profile":
				showUserProfilePage();
				break;
			default:
				console.log("Can't go here.");
		}
	})

	// Form Submissions
	.on("submit","#form-login",e=>{
		e.preventDefault();
		checkLoginForm();
	})


	.on("submit","#add-location-form",e=>{
		e.preventDefault();

		let newid = currentBar().locations.length ?
			currentBar().locations.slice(-1)[0].id+1 :
			0;
		
		currentBar().locations.push({
			"id": newid,
            "lat": +$("#add-location-lat").val(),
            "lng": +$("#add-location-lng").val(),
            "description": $("#add-location-description").val(),
            "img": "https://via.placeholder.com/400x300"
		});

		showBarProfilePage();
	})

	.on("submit","#edit-user-form",e=>{
		e.preventDefault();

		currentUser().name = $("#edit-user-name").val();
		currentUser().email = $("#edit-user-email").val();
		currentUser().password = $("#edit-user-password").val();

		showUserProfilePage();
	})






	// Clicks
	.on("click",".js-logout",e=>{
		e.preventDefault();
		sessionStorage.removeItem("userId");
		checkStorage();
	})
	.on("click",".bar-jump",e=>{
		console.log(e.target)
		sessionStorage.barId = $(e.target).data("id");
		$.mobile.navigate("#page-bar-profile")
	})

	.on("click","[data-activate]",e=>{
		$($(e.target).data("activate"))
			.addClass("active");
	})
	.on("click","[data-deactivate]",e=>{
		console.log(e.target)
		$($(e.target).data("deactivate"))
			.removeClass("active");
	})
	.on("click","[data-toggle]",e=>{
		$($(e.target).data("toggle"))
			.toggleClass("active");
	})

	.on("click",".rem-bar",e=>{
		currentUser().bars =
			currentUser().bars.filter(o=>
				o.id!=$(e.target).data("id")
			);

		$.mobile.navigate("#page-list");
	})





	// Open Edit Forms
	.on("click",".open-edit-user",e=>{
		$("#edit-user-form .modal-body")
			.html(makeEditUserForm(currentUser()));
	})



	$("[data-template]").each((i,o)=>{
		$(o).html( $( $(o).data("template") ).html() );
	})

});
