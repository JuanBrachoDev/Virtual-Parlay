// Checks that 'confirm password' field is equal to 'password' field
function checkConfirmPassword(event){   
    if ($('#password').val() === $('#confirm_password').val()) {
        $('#confirm_password').addClass("valid");
        $('#confirm_password').removeClass("invalid");
    } else {
        $('#confirm_password').addClass("invalid");
        $('#confirm_password').removeClass("valid");
    }
}
