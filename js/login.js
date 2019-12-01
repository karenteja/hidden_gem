const checkLoginForm = () => {
	const username = $("#form-login-username")[0].value;
	const password = $("#form-login-password")[0].value;

	const user = db.find(o =>
		o.username==username &&
		o.password==password);

	if(user) {
		sessionStorage.userId = user.id;
		$("#form-login")[0].reset();
	} else {
		sessionStorage.removeItem('userId');
	}

	checkStorage();
}

const checkStorage = () => {

	const allowedpages = ["#page-login","#page-signup","#bars-list","#page-profile"];
	// Not logged in
	if(sessionStorage.userId===undefined) {
		if(!allowedpages.some(o=>o==location.hash)) {
			$.mobile.navigate("#page-login")
		}
	}
	// Logged in
	else {
		if(allowedpages.some(o=>o==location.hash)) {
			$.mobile.navigate("#page-profile")
		}
	}
}
