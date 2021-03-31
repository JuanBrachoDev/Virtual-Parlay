$(document).ready(function(){
    $('.dropdown-trigger').dropdown();
    $('.modal').modal();
    // Scrolls down to bottom of discussion once DOM is safe to manipulate
    window.scrollTo(0,document.body.scrollHeight);
});

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