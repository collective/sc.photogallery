// https://hacks.mozilla.org/2015/04/es6-in-depth-iterators-and-the-for-of-loop/
jQuery.prototype[Symbol.iterator] = Array.prototype[Symbol.iterator];


$(window).load(() => {
  for (let photogallery of $('.photogallery')) {
    let galleryTop = new Swiper(`#${photogallery.id} .gallery-top`, {
      grabCursor: true,
      navigation: {
        nextEl: `#${photogallery.id} .gallery-top .swiper-button-next`,
        prevEl: `#${photogallery.id} .gallery-top .swiper-button-prev`
      }
    });
    let galleryThumbs = new Swiper(`#${photogallery.id} .gallery-thumbs`, {
      spaceBetween: 10,
      centeredSlides: true,
      slidesPerView: 'auto',
      touchRatio: 0.2,
      slideToClickedSlide: true
    });
    galleryTop.controller.control = galleryThumbs;
    galleryThumbs.controller.control = galleryTop;
  }
});
