class PhotoGallery {
  constructor(el) {
    this.$el = $(el);
    this.proportion = 3 / 2;
    this.bind_events();
    this.fix_image_size();
  }
  $(selector) {
    return $(selector, this.$el);
  }
  bind_events() {
    this.$('.cycle-player').on('cycle-next cycle-prev', this.sync_slideshows.bind(this));
    this.$('.cycle-carrossel .thumb-itens').on('click', this.thumbs_click.bind(this));
  }
  fix_image_size() {
    let max_height, max_width, $player, $imgs;

    // Calc max_with and max_height
    $player = this.$('.cycle-player');
    max_width = $player.width();
    max_height = max_width / this.proportion;
    // Calc max_with and max_height

    $imgs = this.$('.cycle-player img');
    $imgs.css({
      'max-width': max_width,
      'max-height': max_height
    });
  }
  sync_slideshows(e, opts) {
    let index, $player, $slideshows;
    $slideshows = this.$('.cycle-slideshow');
    $slideshows.cycle('goto', opts.currSlide);
  }
  thumbs_click(e) {
    let index, $thumbs, $slideshows;
    e.preventDefault();
    $thumbs = this.$('.cycle-carrossel');
    index = $thumbs.data('cycle.API').getSlideIndex(e.target.parentElement);
    $slideshows = this.$('.cycle-slideshow');
    $slideshows.cycle('goto', index);
  }
}


$(window).load(() => {
  let i, len, ref, slideshow;
  ref = $('.slideshow-container');
  for (i = 0, len = ref.length; i < len; i++) {
    slideshow = ref[i];
    new PhotoGallery(slideshow);
  }
});


module.exports = {
  PhotoGallery
}
