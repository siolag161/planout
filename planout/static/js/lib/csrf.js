(function() {
  var csrfSafeMethod, csrftoken, getCookie;

  getCookie = function(name) {
    var cookie, cookieValue, cookies, i;
    cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      cookies = document.cookie.split(';');
      i = 0;
      while (i < cookies.length) {
        cookie = jQuery.trim(cookies[i]);
        if (cookie.substring(0, name.length + 1) === name + '=') {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
        i++;
      }
    }
    return cookieValue;
  };

  csrftoken = getCookie('csrftoken');

  csrfSafeMethod = function(method) {
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  };

  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader('X-CSRFToken', csrftoken);
      }
    }
  });

}).call(this);

//# sourceMappingURL=csrf.js.map
