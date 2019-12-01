

// HELPERS
// const waitForDB = fn => {
// 	if(!db.length) {
// 		setTimeout(()=>fn(),10);
// 		return false;
// 	} return true;
// }

const checkData = (checker,t=10) => new Promise((resolve,reject) => {
	let c = 0;
	const check = () => ++c>50 ? reject('too many tries') :
		checker() ?
		resolve(checker()) :
		setTimeout(check,t);
	check();
});

const getUser = id => db.find(o=>o.id==id);
const getBar = (u,id) => (u?u:{}).bars.find(o=>o.id==id);

const currentUser = () => getUser(sessionStorage.userId);
const currentBar = () => getBar(currentUser(),sessionStorage.barId);

