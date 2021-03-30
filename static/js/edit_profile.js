$(document).ready(function() {       
    $('#profile_picture').bind('change', function() {
        // Checks if file is bigger than 5MB, shows error message and clears input   
        // in case it is,otherwise it removes the error message if it was showing.
        if(this.files[0].size > 5242880) {
            $('#profile_picture').val("");
            $("#helper_profile_picture").removeClass("hide");
        } else {
            $("#helper_profile_picture").addClass("hide");
        }
        
    });
});