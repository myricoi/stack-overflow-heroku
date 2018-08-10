function clearInputFields(element) {
	element.setAttribute("value","")
}
document.getElementById("email-input").addEventListener("click",function(){clearInputFields(this)})