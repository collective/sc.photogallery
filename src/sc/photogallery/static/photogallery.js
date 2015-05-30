var PhotoGallery = (function() {
  function PhotoGallery() {
    var self = this;
    $('.slideshow-container .cycle-slideshow').on('cycle-next cycle-prev', self, self.sync_slideshows);
    $('.slideshow-container .cycle-carrossel .thumb-itens').on('click', self, self.thumbs_click);
  }
  PhotoGallery.prototype.$ = function(selector, context) {
    var $container;
    $container = $(context).closest('.slideshow-container');
    return $(selector, $container);
  };
  PhotoGallery.prototype.sync_slideshows = function(e, opts) {
    var $slideshows, self;
    self = e.data;
    $slideshows = self.$('.cycle-slideshow', this);
    $slideshows.not(this).cycle('goto', opts.currSlide);
  };
  PhotoGallery.prototype.thumbs_click = function(e) {
    var $slideshows, index, self;
    self = e.data;
    e.preventDefault();
    $slideshow = self.$('.cycle-slideshow', this);
    $thumbs = self.$('.cycle-carrossel', this);
    index = $thumbs.data('cycle.API').getSlideIndex(this);
    $slideshows = self.$('.cycle-slideshow', this);
    $slideshows.cycle('goto', index);
  };
  return PhotoGallery;
})();
$(window).load(function() {
  return new PhotoGallery();
});
