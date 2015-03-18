(function() {
  'use strict';
  if (typeof jQuery === 'undefined') {
    throw new Error('avatar js requires jQuery');
  }

  $(document).ready(function() {
    $('ul.nav li.dropdown').hover((function() {
      $(this).find('.dropdown-menu').stop(true, true).delay(100).fadeIn(300);
    }), function() {
      $(this).find('.dropdown-menu').stop(true, true).delay(100).fadeOut(300);
    });
  });

}).call(this);

//# sourceMappingURL=script.js.map
