$(document).ready(function(){
  let time = 500;
  $(".item-img").hover(function() {
    let img = $(this);
    let src = img.attr('src');
    $(this).attr("src", src.replace('1.jpg', '2.jpg')).css(
      {
        'transition-behavior' : 'normal',
        'transition-duration' : '0.1s',
        'transition-timing-function' : 'linear',
        'transition-delay' : '0s',
        'transition-property' : 'opacity'
      }
  )}, 
  function() {
    let img = $(this);
    let src = img.attr('src');
    $(this).attr("src", src.replace('2.jpg', '1.jpg')).css(
      {
        'transition-behavior' : 'normal',
        'transition-duration' : '0.1s',
        'transition-timing-function' : 'linear',
        'transition-delay' : '0s',
        'transition-property' : 'opacity'
      }
  )
  }
  );
});