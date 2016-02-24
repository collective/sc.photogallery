var PhotoGallery = (function() {
  function PhotoGallery(el) {
    var self = this;
    self.$el = $(el);
    self.proportion = 3 / 2;
    self.bind_events();
    self.fix_image_size();
  }
  PhotoGallery.prototype.$ = function(selector) {
    var self = this;
    return $(selector, self.$el);
  };
  PhotoGallery.prototype.bind_events = function() {
    var self = this;
    self.$('.cycle-player').on('cycle-next cycle-prev', self, self.sync_slideshows);
    self.$('.cycle-carrossel .thumb-itens').on('click', self, self.thumbs_click);
  };
  PhotoGallery.prototype.fix_image_size = function() {
    var self, max_height, max_width, $player, $imgs;
    self = this;

    // Calc max_with and max_height
    $player = self.$('.cycle-player');
    max_width = $player.width();
    max_height = max_width / self.proportion;
    // Calc max_with and max_height

    $imgs = self.$('.cycle-player img');
    $imgs.css({
      'max-width': max_width,
      'max-height': max_height
    });
  };

  PhotoGallery.prototype.sync_slideshows = function(e, opts) {
    var self, index, $player, $slideshows;
    self = e.data;
    $slideshows = self.$('.cycle-slideshow');
    $slideshows.cycle('goto', opts.currSlide);
  };

  PhotoGallery.prototype.thumbs_click = function(e) {
    var self, index, $thumbs, $slideshows;
    self = e.data;
    e.preventDefault();
    $thumbs = self.$('.cycle-carrossel');
    index = $thumbs.data('cycle.API').getSlideIndex(this);
    $slideshows = self.$('.cycle-slideshow');
    $slideshows.cycle('goto', index);
  };
  return PhotoGallery;
})();
$(window).load(function() {
  var i, len, ref, slideshow;
  ref = $('.slideshow-container');
  for (i = 0, len = ref.length; i < len; i++) {
    slideshow = ref[i];
    new PhotoGallery(slideshow);
  }
});
