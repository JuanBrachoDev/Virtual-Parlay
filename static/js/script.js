$(document).ready(function(){
    $(".sidenav").sidenav({edge: "right"});
    $('.dropdown-trigger').dropdown();
});

$(function(){
  $( ".post" ).bind( "taphold", tapholdHandler);
 
  function tapholdHandler( event ){
    $( ".post-options-button" ).click();
  }
});