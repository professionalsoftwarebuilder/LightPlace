//alert('begin main');
//$('.zi-show').zoomImage();
//alert('na zoomimg in main');
$('.zi-show-zi-small-img:first-of-type').css({'border': 'solid 3px #951b25', 'padding': '2px'})
$('.zi-show-zi-small-img:first-of-type').attr('alt', 'now').siblings().removeAttr('alt')

/// Wanneer op de thumbnail wordt geclicked
$('.zi-show-zi-small-img').click(function () {
  /// Stop url van thumbnail in active (grote image)  
  $('#zi-show-img').attr('src', $(this).attr('src'))
  var theHeight = $('#zi-show-img').height();
  var theWidth = $('#zi-show-img').width();
  /// Stop url van thumbnail in vergrootglas image (het onthefly image) 
  $('#big-img').attr('src', $(this).attr('src'))
  $('#big-img').height(theHeight * 5);
  $('#big-img').width(theWidth * 5);
  $(this).attr('alt', 'now').siblings().removeAttr('alt')
  /// Geef het geclickte image een andere border??
  $(this).css({'border': 'solid 3px #951b25', 'padding': '2px'}).siblings().css({'border': 'none', 'padding': '0'})
  /// Als meer dan 4 thumbnail sin imageroll div dan corousel achtig ding doen
  if ($('#zi-small-img-roll').children().length > 4) {
    if ($(this).index() >= 3 && $(this).index() < $('#zi-small-img-roll').children().length - 1){
      $('#zi-small-img-roll').css('left', -($(this).index() - 2) * 76 + 'px')
    } else if ($(this).index() == $('#zi-small-img-roll').children().length - 1) {
      $('#zi-small-img-roll').css('left', -($('#zi-small-img-roll').children().length - 4) * 76 + 'px')
    } else {
      $('#zi-small-img-roll').css('left', '0')
    }
  }
  //$.fn.zoomImage.remove();
  //mySmartPhoto.close();
  //mySmartPhoto = $('.zi-show').zoomImage();
  //$('#pietjepuk').css({height: theHeight});
  //$('#pietjepuk').css({height: '1000px'});
  $('#pietjepuk').height(theHeight);
  $('#pietjepuk').width(theWidth);
   $('.zi-show').height(theHeight);
  $('.zi-show').width(theWidth);
  //$('#pietjepuk').remove();
  //$('.zi-show').zoomImage();
  //$('.zi-show').css({height: '1000px'});
  //$('#zi-show-img').css({height: '1000px'});
})

// Klik op '>' Volgende
/// alt = now schijnt gebruikt te worden om thumb als actief aan te merken?
$('#next-img').click(function (){
  $('#zi-show-img').attr('src', $(".zi-show-zi-small-img[alt='now']").next().attr('src'))
  $('#big-img').attr('src', $(".zi-show-zi-small-img[alt='now']").next().attr('src'))
  $(".zi-show-zi-small-img[alt='now']").next().css({'border': 'solid 1px #951b25', 'padding': '2px'}).siblings().css({'border': 'none', 'padding': '0'})
  $(".zi-show-zi-small-img[alt='now']").next().attr('alt', 'now').siblings().removeAttr('alt')
  if ($('#zi-small-img-roll').children().length > 4) {
    if ($(".zi-show-zi-small-img[alt='now']").index() >= 3 && $(".zi-show-zi-small-img[alt='now']").index() < $('#zi-small-img-roll').children().length - 1){
      $('#zi-small-img-roll').css('left', -($(".zi-show-zi-small-img[alt='now']").index() - 2) * 76 + 'px')
    } else if ($(".zi-show-zi-small-img[alt='now']").index() == $('#zi-small-img-roll').children().length - 1) {
      $('#zi-small-img-roll').css('left', -($('#zi-small-img-roll').children().length - 4) * 76 + 'px')
    } else {
      $('#zi-small-img-roll').css('left', '0')
    }
  }
})
// Klik op '<' Vorige
$('#prev-img').click(function (){
  $('#zi-show-img').attr('src', $(".zi-show-zi-small-img[alt='now']").prev().attr('src'))
  $('#big-img').attr('src', $(".zi-show-zi-small-img[alt='now']").prev().attr('src'))
  $(".zi-show-zi-small-img[alt='now']").prev().css({'border': 'solid 1px #951b25', 'padding': '2px'}).siblings().css({'border': 'none', 'padding': '0'})
  $(".zi-show-zi-small-img[alt='now']").prev().attr('alt', 'now').siblings().removeAttr('alt')
  if ($('#zi-small-img-roll').children().length > 4) {
    if ($(".zi-show-zi-small-img[alt='now']").index() >= 3 && $(".zi-show-zi-small-img[alt='now']").index() < $('#zi-small-img-roll').children().length - 1){
      $('#zi-small-img-roll').css('left', -($(".zi-show-zi-small-img[alt='now']").index() - 2) * 76 + 'px')
    } else if ($(".zi-show-zi-small-img[alt='now']").index() == $('#zi-small-img-roll').children().length - 1) {
      $('#zi-small-img-roll').css('left', -($('#zi-small-img-roll').children().length - 4) * 76 + 'px')
    } else {
      $('#zi-small-img-roll').css('left', '0')
    }
  }
})

//alert('eind main');

