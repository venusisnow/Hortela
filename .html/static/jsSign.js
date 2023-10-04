function validateForm(){
	const url = new URLSearchParams(window.location.search);
	const val = url.get('error');

	if (val === '1') {
		var e = document.getElementById("email");
		
		e.style.border = ("solid 2px red");
	};
	
	oldValues(url)
};

function oldValues(url){
	var n = document.getElementById("nome");
	var s = document.getElementById("pass");
	
	var vn = url.get('n');
	nome.value = vn
	var vn = url.get('p');
	s.value = vn
}