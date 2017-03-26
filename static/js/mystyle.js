// $('#navtabs').find('li').tooltipsy({title: 'aria-label'});
function tog(v){return v?'addClass':'removeClass';}
$(document).ready(function(){

  $('.search-input').focus(function(){
      $(this).parent().addClass('focus');
      $(this).prev().children('i').css('opacity','0.9');
  }).blur(function(){
      $(this).parent().removeClass('focus');
      $(this).prev().children('i').css('opacity','0.5');
  });
  $('.search-form').on('input', '.search-input', function(){
    $(this)[tog(this.value)]('x');
    }).on('mousemove', '.x', function( e ){
        $(this)[tog(this.offsetWidth-18 < e.clientX-this.getBoundingClientRect().left)]('onX');
    }).on('touchstart click', '.onX', function( ev ){
        ev.preventDefault();
        $(this).removeClass('x onX').val('').change();
  });

  $(".search-form").submit(function() {
    var query = $(this).find("input[name=query]").val();
    if($.trim(query) == "") {
        alert("Please enter a query.");
        return false;
    }
  });

});
