// Initializes materialize components
$(document).ready(function(){
    $(".sidenav").sidenav({edge: "right"});
});

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