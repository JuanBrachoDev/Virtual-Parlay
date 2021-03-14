$(document).ready(function(){
    $(".sidenav").sidenav({edge: "right"});
    $('.dropdown-trigger').dropdown();
    $('.collapsible').collapsible();
});

$(function(){
  $( ".post" ).bind( "taphold", tapholdHandler);
 
  function tapholdHandler( event ){
    $( ".post-options-button" ).click();
  }
});


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

// Hides topic's area and shows edit form
function showTopicEdit(){   
    $('#edit_topic_area').removeClass("hide");
    $('#topic_area').addClass("hide");
}

// Hides topic's form and shows area
function hideTopicEdit(){   
    $('#topic_area').removeClass("hide");
    $('#edit_topic_area').addClass("hide");
}