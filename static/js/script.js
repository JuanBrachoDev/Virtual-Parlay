// Initializes materialize components
$(document).ready(function(){
    $(".sidenav").sidenav({edge: "right"});
    $('.dropdown-trigger').dropdown();
    $('.collapsible').collapsible();
});

// Adds taphold events to posts
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

// Hides post's text and shows edit form
function showPostEdit(button){
    $(`#edit_post_area_${$(button).data("post")}`).removeClass("hide");
    $(`#post_text_${$(button).data("post")}`).addClass("hide");
}

// Hides post's form and shows text
function hidePostEdit(button){   
    $(`#post_text_${$(button).data("post")}`).removeClass("hide");
    $(`#edit_post_area_${$(button).data("post")}`).addClass("hide");
}

// Expands search field
function showSearchField(searchField){
    $(searchField).removeClass("search-load");
    $(searchField).removeClass("search-hidden");
    $(searchField).addClass("search-shown");
}

// Shrinks search field
function hideSearchField(searchField){   
    $(searchField).removeClass("search-shown");
    $(searchField).addClass("search-hidden");
    $(searchField).val("");
}