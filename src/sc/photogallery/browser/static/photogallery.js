var PhotoGallery = (function() {
  function PhotoGallery() {
    var self = this;
    $('.slideshow-container .cycle-player').on('cycle-next cycle-prev', self, self.sync_slideshows);
    $('.slideshow-container .cycle-carrossel .thumb-itens').on('click', self, self.thumbs_click);
    $('.slideshow-container .cycle-player img').each(function() {
      var $img = $(this);
      if ($img.height() > $img.width()) {
        $img.css('width', 'auto');
      }
    });
  }
  PhotoGallery.prototype.$ = function(selector, context) {
    var $container;
    $container = $(context).closest('.slideshow-container');
    return $(selector, $container);
  };
  PhotoGallery.prototype.sync_slideshows = function(e, opts) {
    var $description, $pager, self;
    self = e.data;
    $description = self.$('.cycle-description', this);
    $pager = self.$('.cycle-pager', this);
    $description.cycle('goto', opts.currSlide);
    $pager.cycle('goto', opts.currSlide -1); // this is weird
  };
  PhotoGallery.prototype.thumbs_click = function(e) {
    var $slideshows, index, self;
    self = e.data;
    e.preventDefault();
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
