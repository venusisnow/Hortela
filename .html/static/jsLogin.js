function validateForm(){
	const url = new URLSearchParams(window.location.search);
	const val = url.get('error');

	if (val === '1') {
		var n = document.getElementById("email");
		var s = document.getElementById("pass");
		
		n.style.border = ("solid 2px red");
		s.style.border = ("solid 2px red");
		
		console.log("ayo")
	}
};