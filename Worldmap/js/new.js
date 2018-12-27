$(document).ready(function(){
  $(".distribution-map button").hover(function() {
    $(this).find("span").animate({opacity: "show", top: "-65"}, "slow");
  }, function() {
    $(this).find("span").animate({opacity: "hide", top: "-85"}, "fast");
  });

});
