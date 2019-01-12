$(".login-form").hide();
$(".login").css("background", "none");

$(".login").click(function(){
  $(".signup-form").hide();
  $(".login-form").show();
  $(".signup").css("background", "none");
  $(".login").css("background", "#4CAF50");
});

$(".signup").click(function(){
  $(".signup-form").show();
  $(".login-form").hide();
  $(".login").css("background", "none");
  $(".signup").css("background", "#4CAF50");
});

$(".btn").click(function(){
  $(".input").val("");
});

var logInButton = document.getElementById('log')
var signUpButton = document.getElementById('sign')

logInButton.addEventListener('click', () => {
	if (!logInButton.classList.contains('whiteText'))
		logInButton.classList.add('whiteText')
	if (signUpButton.classList.contains('whiteText'))
		signUpButton.classList.remove('whiteText')
})

signUpButton.addEventListener('click', () => {
	if (!signUpButton.classList.contains('whiteText'))
		signUpButton.classList.add('whiteText')
	if (logInButton.classList.contains('whiteText'))
		logInButton.classList.remove('whiteText')
})

signUpButton.classList.add('whiteText')