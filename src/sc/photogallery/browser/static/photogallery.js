$(window).load(function() {
  var i, len, ref, slideshow;
  ref = $('.slideshow-container');
  for (i = 0, len = ref.length; i < len; i++) {
    slideshow = ref[i];
    new cycle2SlideShow(slideshow);
  }
});
