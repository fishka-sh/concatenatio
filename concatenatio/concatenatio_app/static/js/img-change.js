$(document).ready(function(){
  $(".item-img").hover(function() {
    let img = $(this);
    let src = img.attr('src');
    $(this).attr("src", src.replace('1.jpg', '2.jpg'));
    $(this).animate(0.25);
  }, 
  function(){
    let img = $(this);
    let src = img.attr('src');
    $(this).attr("src", src.replace('2.jpg', '1.jpg'))
  });
});