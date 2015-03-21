(function() {
  'use strict';
  var EventPush, SplitDateTime;

  if (typeof jQuery === 'undefined') {
    throw new Error('avatar js requires jQuery');
  }

  SplitDateTime = (function() {
    function SplitDateTime($element) {
      this.$container = $element;
      this.$dateInput = this.$container.find('.input-group.date');
      this.$timeInput = this.$container.find('.input-group.time');
      this.dateOpts = {
        format: 'dd/mm/yyyy',
        autoclose: true
      };
      this.timeOpts = {
        "default": 'now',
        autoclose: true,
        minutestep: 5,
        twelvehour: true
      };
      this.init();
    }

    SplitDateTime.prototype.init = function() {
      return this.addListener();
    };

    SplitDateTime.prototype.addListener = function() {
      this.datePicker = this.$dateInput.datepicker(this.dateOpts).on('changeDate', $.proxy(this.dateChange, this));
      return this.timePicker = this.$timeInput.clockpicker(this.timeOpts);
    };

    SplitDateTime.prototype.dateChange = function(e) {
      console.log("dateChanged");
      e.preventDefault();
      this.$timeInput.clockpicker().clockpicker('show');
    };

    return SplitDateTime;

  })();

  EventPush = function($element) {
    this.$container = $element;
    this.$locationPreview = $('#location-map-preview');
    this.$formSubmit = $('#event-form-submit');
    this.$locationInput = $('#id_location');
    this.$event_form = this.$container.find('form');
    this.$startSplit = new SplitDateTime(this.$container.find('#div_id_start_time'));
    this.$endSplit = new SplitDateTime(this.$container.find('#div_id_end_time'));
    'timing setup';
    this.$timeOpts = {
      "default": 'now',
      autoclose: true,
      minutestep: 5,
      twelvehour: true
    };
    'location setup';
    this.$location_fields = this.$event_form.find(".superlocation input");
    this.$superloc_input = this.$event_form.find("#div_id_location");
    this.$superloc_field = this.$event_form.find("#id_location");
    this.$hid_toggle_fields = this.$event_form.find(".toggle-field.hid");
    this.$locResetButton = this.$container.find('.location-reset');
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
      this.$locResetButton.on('click', $.proxy(this.resetLocation, this));
    },
    resetLocationData: function() {
      this.$location_fields.val("");
      this.$superloc_field.val("");
    },
    hideLocationFields: function() {
      this.$superloc_input.show("fast");
      this.$hid_toggle_fields.hide("fast");
      this.$mapCanvasWrapper.addClass('hidden');
    },
    resetLocation: function(e) {
      this.hideLocationFields();
      e.preventDefault();
      this.resetLocationData();
    },
    submit: function(event) {},
    locationChange: function(event, result) {
      this.$superloc_input.hide("fast");
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
