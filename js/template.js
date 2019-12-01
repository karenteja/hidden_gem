// Template functions

// currying, reduce
const templater = tf => oa =>
	(Array.isArray(oa)?oa:[oa])
	.reduce((r,o,i,a)=>r+tf(o,i,a),'');

// backtick templates
const makeUserList = templater(o=>`
	<div class="user">
		${o.name}
		<div class="bars-list">
			${makeBarsList(o.bars)}
		</div>
	</div>
`);

const makeBarsList = templater(o=>`
	<div class="bar-item card flex-parent">
		<div class="flex-none bar-icon"><img src="${o.img}" alt="${o.bar_name}"></div>
		<div class="flex-child bar-name">${o.bar_name}</div>
		<div class="flex-none list-btn bar-jump" data-id="${o.id}">&gt;</div>
	</div>
`);

const makeBarProfile = templater(o=>`
	<div class="bar-image">
		<img src="${o.img}" alt="${o.name}" class="media-image">
	</div>
	<div class="bar-details">
		<div>${o.bar_name}</div>
		<div>${o.area}</div>
		<div><a href="#" class="rem-bar" data-id="${o.id}">delete</a></div>
	</div>
	
`);

const makeUserProfile = templater(o=>`
	<div class="profile-pic"><img src="${o.img}" alt="${o.name}" /></div>
	<h2>${o.name}</h2>
	<dl class="profile-specs container">
		
		<dt>Email</dt><dd>${o.email}</dd>
		<dt>Bars</dt><dd>${o.bars.length}</dd>
	</dl>
`);

// console.log(makeUserList([{name:'Me'},{name:'You'}]));



const makeEditUserForm = templater(o=>`
<div class="form-control">
	<label class="form-label" for="edit-user-name">Name</label>
	<input class="form-input" type="text" id="edit-user-name" data-role="none" value="${o.name}">
</div>
<div class="form-control">
	<label class="form-label" for="edit-user-breed">Email</label>
	<input class="form-input" type="text" id="edit-user-email" data-role="none" value="${o.email}">
</div>
<div class="form-control">
	<label class="form-label" for="edit-user-breed">Password</label>
	<input class="form-input" type="password" id="edit-user-password" data-role="none" value="${o.password}">
</div>
`);
