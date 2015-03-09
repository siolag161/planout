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
    this.$event_form = this.$container.find('form');
    this.$event_toggle_elems = this.$event_form.find(".toggle-field");
    this.$map = void 0;
    this.init();
  };

  EventPush.prototype = {
    constructor: EventPush,
    init: function() {
      this.addListener();
    },
    addListener: function() {
      this.$locationInput.geocomplete({
        map: ".map_canvas",
        details: '.superlocation',
        detailsAttribute: "data-geo",
        types: ["geocode", "establishment"],
        componentRestrictions: {
          country: 'vn'
        }
      }).on('geocode:result', $.proxy(this.locationChange, this));
    },
    submit: function() {},
    locationChange: function(event, result) {
      this.$event_toggle_elems.removeClass('hidden');
      if (!this.$map) {
        this.$map = this.$locationInput.geocomplete("map");
      }
      google.maps.event.trigger(this.$map, 'resize');
    },
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
