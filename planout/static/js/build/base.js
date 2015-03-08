
/*!
 *#
 */

(function() {
  'use strict';
  if (typeof jQuery === 'undefined') {
    throw new Error('base js requires jQuery');
  }

  $.base = {};


  /* --------------------
   * - AdminLTE Options -
   * --------------------
   * Modify these options to suit your implementation
   */

  $.base.options = {
    navbarMenuSlimscroll: true,
    navbarMenuSlimscrollWidth: '3px',
    navbarMenuHeight: '200px',
    sidebarToggleSelector: '[data-toggle=\'offcanvas\']',
    sidebarPushMenu: true,
    sidebarSlimScroll: true,
    enableBoxRefresh: true,
    enableBSToppltip: true,
    BSTooltipSelector: '[data-toggle=\'tooltip\']',
    enableFastclick: true,
    enableBoxWidget: true,
    boxWidgetOptions: {
      boxWidgetIcons: {
        collapse: 'fa fa-minus',
        open: 'fa fa-plus',
        remove: 'fa fa-times'
      },
      boxWidgetSelectors: {
        remove: '[data-widget="remove"]',
        collapse: '[data-widget="collapse"]'
      }
    },
    directChat: {
      enable: true,
      contactToggleSelector: '[data-widget="chat-pane-toggle"]'
    },
    colors: {
      lightBlue: '#3c8dbc',
      red: '#f56954',
      green: '#00a65a',
      aqua: '#00c0ef',
      yellow: '#f39c12',
      blue: '#0073b7',
      navy: '#001F3F',
      teal: '#39CCCC',
      olive: '#3D9970',
      lime: '#01FF70',
      orange: '#FF851B',
      fuchsia: '#F012BE',
      purple: '#8E24AA',
      maroon: '#D81B60',
      black: '#222222',
      gray: '#d2d6de'
    }
  };


  /* ------------------
   * - Implementation -
   * ------------------
   * The next block of code implements AdminLTE's
   * functions and plugins as specified by the
   * options above.
   */

  $(function() {
    var o;
    o = $.base.options;
    $.base.layout.activate();
    $.base.tree('.sidebar');
    if (o.navbarMenuSlimscroll && typeof $.fn.slimscroll !== 'undefined') {
      $('.navbar .menu').slimscroll({
        height: '200px',
        alwaysVisible: false,
        size: '3px'
      }).css('width', '100%');
    }
    if (o.sidebarPushMenu) {
      $.base.pushMenu(o.sidebarToggleSelector);
    }
    if (o.enableBSToppltip) {
      $(o.BSTooltipSelector).tooltip();
    }
    if (o.enableBoxWidget) {
      $.base.boxWidget.activate();
    }
    if (o.enableFastclick && typeof FastClick !== 'undefined') {
      FastClick.attach(document.body);
    }
    if (o.directChat.enable) {
      $(o.directChat.contactToggleSelector).click(function() {
        var box;
        box = $(this).parents('.direct-chat').first();
        box.toggleClass('direct-chat-contacts-open');
      });
    }

    /*
     * INITIALIZE BUTTON TOGGLE
     * ------------------------
     */
    $('.btn-group[data-toggle="btn-toggle"]').each(function() {
      var group;
      group = $(this);
      $(this).find('.btn').click(function(e) {
        group.find('.btn.active').removeClass('active');
        $(this).addClass('active');
        e.preventDefault();
      });
    });
  });


  /* ----------------------
   * - AdminLTE Functions -
   * ----------------------
   * All AdminLTE functions are implemented below.
   */


  /* prepareLayout
   * =============
   * Fixes the layout height in case min-height fails.
   *
   * @type Object
   * @usage $.base.layout.activate()
   *        $.base.layout.fix()
   *        $.base.layout.fixSidebar()
   */

  $.base.layout = {
    activate: function() {
      var _this;
      _this = this;
      _this.fix();
      _this.fixSidebar();
      $(window, '.wrapper').resize(function() {
        _this.fix();
        _this.fixSidebar();
      });
    },
    fix: function() {
      var neg, sidebar_height, window_height;
      neg = $('.main-header').outerHeight() + $('.main-footer').outerHeight();
      window_height = $(window).height();
      sidebar_height = $('.sidebar').height();
      if ($('body').hasClass('fixed')) {
        $('.content-wrapper, .right-side').css('min-height', window_height - $('.main-footer').outerHeight());
      } else {
        if (window_height >= sidebar_height) {
          $('.content-wrapper, .right-side').css('min-height', window_height - neg);
        } else {
          $('.content-wrapper, .right-side').css('min-height', sidebar_height);
        }
      }
    },
    fixSidebar: function() {
      if (!$('body').hasClass('fixed')) {
        if (typeof $.fn.slimScroll !== 'undefined') {
          $('.sidebar').slimScroll({
            destroy: true
          }).height('auto');
        }
        return;
      } else if (typeof $.fn.slimScroll === 'undefined' && console) {
        console.error('Error: the fixed layout requires the slimscroll plugin!');
      }
      if ($.base.options.sidebarSlimScroll) {
        if (typeof $.fn.slimScroll !== 'undefined') {
          $('.sidebar').slimScroll({
            destroy: true
          }).height('auto');
          $('.sidebar').slimscroll({
            height: $(window).height() - $('.main-header').height() + 'px',
            color: 'rgba(0,0,0,0.2)',
            size: '3px'
          });
        }
      }
    }
  };


  /* PushMenu()
   * ==========
   * Adds the push menu functionality to the sidebar.
   *
   * @type Function
   * @usage: $.base.pushMenu("[data-toggle='offcanvas']")
   */

  $.base.pushMenu = function(toggleBtn) {
    $(toggleBtn).click(function(e) {
      e.preventDefault();
      $('body').toggleClass('sidebar-collapse');
      $('body').toggleClass('sidebar-open');
    });
    $('.content-wrapper').click(function() {
      if ($(window).width() <= 767 && $('body').hasClass('sidebar-open')) {
        $('body').removeClass('sidebar-open');
      }
    });
  };


  /* Tree()
   * ======
   * Converts the sidebar into a multilevel
   * tree view menu.
   *
   * @type Function
   * @Usage: $.base.tree('.sidebar')
   */

  $.base.tree = function(menu) {
    $('li a', $(menu)).click(function(e) {
      var $this, checkElement, parent, parent_li, ul;
      $this = $(this);
      checkElement = $this.next();
      if (checkElement.is('.treeview-menu') && checkElement.is(':visible')) {
        checkElement.slideUp('normal', function() {
          checkElement.removeClass('menu-open');
        });
        checkElement.parent('li').removeClass('active');
      } else if (checkElement.is('.treeview-menu') && !checkElement.is(':visible')) {
        parent = $this.parents('ul').first();
        ul = parent.find('ul:visible').slideUp('normal');
        ul.removeClass('menu-open');
        parent_li = $this.parent('li');
        checkElement.slideDown('normal', function() {
          checkElement.addClass('menu-open');
          parent.find('li.active').removeClass('active');
          parent_li.addClass('active');
        });
      }
      if (checkElement.is('.treeview-menu')) {
        e.preventDefault();
      }
    });
  };


  /* BoxWidget
   * =========
   * BoxWidget is plugin to handle collapsing and
   * removing boxes from the screen.
   *
   * @type Object
   * @usage $.base.boxWidget.activate()
   *								Set all of your option in the main $.base.options object
   */

  $.base.boxWidget = {
    activate: function() {
      var o, _this;
      o = $.base.options;
      _this = this;
      $(o.boxWidgetOptions.boxWidgetSelectors.collapse).click(function(e) {
        e.preventDefault();
        _this.collapse($(this));
      });
      $(o.boxWidgetOptions.boxWidgetSelectors.remove).click(function(e) {
        e.preventDefault();
        _this.remove($(this));
      });
    },
    collapse: function(element) {
      var bf, box;
      box = element.parents('.box').first();
      bf = box.find('.box-body, .box-footer');
      if (!box.hasClass('collapsed-box')) {
        element.children('.fa-minus').removeClass('fa-minus').addClass('fa-plus');
        bf.slideUp(300, function() {
          box.addClass('collapsed-box');
        });
      } else {
        element.children('.fa-plus').removeClass('fa-plus').addClass('fa-minus');
        bf.slideDown(300, function() {
          box.removeClass('collapsed-box');
        });
      }
    },
    remove: function(element) {
      var box;
      box = element.parents('.box').first();
      box.slideUp();
    },
    options: $.base.options.boxWidgetOptions
  };


  /* ------------------
   * - Custom Plugins -
   * ------------------
   * All custom plugins are defined below.
   */


  /*
   * BOX REFRESH BUTTON
   * ------------------
   * This is a custom plugin to use with the compenet BOX. It allows you to add
   * a refresh button to the box. It converts the box's state to a loading state.
   *
   *	@type plugin
   * @usage $("#box-widget").boxRefresh( options );
   */

  (function($) {
    $.fn.boxRefresh = function(options) {
      var done, overlay, settings, start;
      settings = $.extend({
        trigger: '.refresh-btn',
        source: '',
        onLoadStart: function(box) {},
        onLoadDone: function(box) {}
      }, options);
      overlay = $('<div class="overlay"></div><div class="loading-img"></div>');
      start = function(box) {
        box.append(overlay);
        settings.onLoadStart.call(box);
      };
      done = function(box) {
        box.find(overlay).remove();
        settings.onLoadDone.call(box);
      };
      return this.each(function() {
        var box, rBtn;
        if (settings.source === '') {
          if (console) {
            console.log('Please specify a source first - boxRefresh()');
          }
          return;
        }
        box = $(this);
        rBtn = box.find(settings.trigger).first();
        rBtn.click(function(e) {
          e.preventDefault();
          start(box);
          box.find('.box-body').load(settings.source, function() {
            done(box);
          });
        });
      });
    };
  })(jQuery);


  /*
   * TODO LIST CUSTOM PLUGIN
   * -----------------------
   * This plugin depends on iCheck plugin for checkbox and radio inputs
   *
   * @type plugin
   * @usage $("#todo-widget").todolist( options );
   */

  (function($) {
    $.fn.todolist = function(options) {
      var settings;
      settings = $.extend({
        onCheck: function(ele) {},
        onUncheck: function(ele) {}
      }, options);
      return this.each(function() {
        if (typeof $.fn.iCheck !== 'undefined') {
          $('input', this).on('ifChecked', function(event) {
            var ele;
            ele = $(this).parents('li').first();
            ele.toggleClass('done');
            settings.onCheck.call(ele);
          });
          $('input', this).on('ifUnchecked', function(event) {
            var ele;
            ele = $(this).parents('li').first();
            ele.toggleClass('done');
            settings.onUncheck.call(ele);
          });
        } else {
          $('input', this).on('change', function(event) {
            var ele;
            ele = $(this).parents('li').first();
            ele.toggleClass('done');
            settings.onCheck.call(ele);
          });
        }
      });
    };
  })(jQuery);

  (function($) {
    $('a#modal-login-button').on('click', function(event) {
      $('#signup-modal').modal('toggle');
    });
    return $('a#modal-signup-button').on('click', function(event) {
      $('#login-modal').modal('toggle');
    });
  })(jQuery);

}).call(this);

//# sourceMappingURL=base.js.map
