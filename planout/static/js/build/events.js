(function() {
  'use strict';
  var EventPush;

  if (typeof jQuery === 'undefined') {
    throw new Error('avatar js requires jQuery');
  }

  EventPush = function($element) {
    this.$container = $element;
    this.$locationPreview = $('#location-map-preview');
    this.$formSubmit = $('#event-form-submit');
    this.$locationInput = $('#id_location');
    this.init();
  };

  EventPush.prototype = {
    constructor: EventPush,
    init: function() {
      this.addListener();
    },
    addListener: function() {
      this.$locationInput.geocomplete({
        details: '#superlocation',
        detailsAttribute: "data-geo"
      }).on('geocode:result', $.proxy(this.locationChange, this));
    },
    submit: function() {},
    locationChange: function(event, result) {},
    ensureTime: function() {}
  };

  (function($) {
    return $(document).ready(function() {
      var $form_wrapper;
      $form_wrapper = $('#event_form_wrapper');
      if ($form_wrapper.length) {
        new EventPush($form_wrapper);
      }
    });
  })(jQuery);

}).call(this);

//# sourceMappingURL=events.js.map
