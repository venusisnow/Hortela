function checkForHeader(){
	var cookie = document.getElementById("uVar").innerHTML;
		var putPreset = document.getElementById("userProfileHeaderDiv");
	
	if(cookie == "None"){
		var signPreset = document.getElementById("userSignUpPreset");
		
		putPreset.innerHTML = signPreset.innerHTML;
	}else{
		var profilePreset = document.getElementById("userLogoutPreset");
		
		putPreset.innerHTML = profilePreset.innerHTML;
	}
}