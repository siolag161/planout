(function() {
  'use strict';
  if (typeof jQuery === 'undefined') {
    throw new Error('avatar js requires jQuery');
  }

  (function($) {
    return $(".input-group.date").datetimepicker({
      format: 'dd/mm/yyyy hh:ii',
      autoclose: true,
      pickerPosition: 'top-left',
      startDate: '+0d',
      showMeridian: true
    });
  })(jQuery);

  $(document).ready(function() {
    $('ul.nav li.dropdown').hover((function() {
      $(this).find('.dropdown-menu').stop(true, true).delay(100).fadeIn(300);
    }), function() {
      $(this).find('.dropdown-menu').stop(true, true).delay(100).fadeOut(300);
    });
  });

}).call(this);

//# sourceMappingURL=script.js.map
