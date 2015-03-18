(function() {
  'use strict';
  var EventPush;

  if (typeof jQuery === 'undefined') {
    throw new Error('avatar js requires jQuery');
  }

  (function($) {
    $(".input-group.date").datepicker({
      format: 'dd/mm/yyyy',
      autoclose: true,
      pickerPosition: 'auto',
      startDate: '+0d',
      showMeridian: true
    });
    return $(".input-group.time").clockpicker({
      "default": 'now',
      autoclose: true,
      minutestep: 5,
      twelvehour: true
    });
  })(jQuery);

  EventPush = function($element) {
    this.$container = $element;
    this.$locationPreview = $('#location-map-preview');
    this.$formSubmit = $('#event-form-submit');
    this.$locationInput = $('#id_location');
    this.$event_form = this.$container.find('form');
    this.$location_fields = this.$event_form.find("input[type=text].superlocation");
    this.$hid_toggle_fields = this.$event_form.find(".toggle-field.hid");
    this.$resetBtn = this.$container.find('.location-reset');
    this.$mapCanvasWrapper = this.$container.find('#google_map_canvas_wrapper');
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
      this.$resetBtn.on('click', $.proxy(this.resetLocation, this));
    },
    resetLocationData: function() {
      this.$location_fields.val("");
    },
    hideLocationFields: function() {
      this.$hid_toggle_fields.hide("fast");
      this.$mapCanvasWrapper.addClass('hidden');
    },
    resetLocation: function() {
      this.hideLocationFields();
      this.resetLocationData();
    },
    submit: function(event) {},
    locationChange: function(event, result) {
      this.$hid_toggle_fields.show("fast");
      this.$mapCanvasWrapper.removeClass('hidden');
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
