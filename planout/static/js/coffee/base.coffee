###!
##
###

'use strict'
#Make sure jQuery has been loaded before app.js
if typeof jQuery == 'undefined'
  throw new Error('base js requires jQuery')


$.base = {}

### --------------------
# - AdminLTE Options -
# --------------------
# Modify these options to suit your implementation
###

$.base.options =
  navbarMenuSlimscroll: true
  navbarMenuSlimscrollWidth: '3px'
  navbarMenuHeight: '200px'
  sidebarToggleSelector: '[data-toggle=\'offcanvas\']'
  sidebarPushMenu: true
  sidebarSlimScroll: true
  enableBoxRefresh: true
  enableBSToppltip: true
  BSTooltipSelector: '[data-toggle=\'tooltip\']'
  enableFastclick: true
  enableBoxWidget: true
  boxWidgetOptions:
    boxWidgetIcons:
      collapse: 'fa fa-minus'
      open: 'fa fa-plus'
      remove: 'fa fa-times'
    boxWidgetSelectors:
      remove: '[data-widget="remove"]'
      collapse: '[data-widget="collapse"]'
  directChat:
    enable: true
    contactToggleSelector: '[data-widget="chat-pane-toggle"]'
  colors:
    lightBlue: '#3c8dbc'
    red: '#f56954'
    green: '#00a65a'
    aqua: '#00c0ef'
    yellow: '#f39c12'
    blue: '#0073b7'
    navy: '#001F3F'
    teal: '#39CCCC'
    olive: '#3D9970'
    lime: '#01FF70'
    orange: '#FF851B'
    fuchsia: '#F012BE'
    purple: '#8E24AA'
    maroon: '#D81B60'
    black: '#222222'
    gray: '#d2d6de'

### ------------------
# - Implementation -
# ------------------
# The next block of code implements AdminLTE's
# functions and plugins as specified by the
# options above.
###

$ ->
  #Easy access to options
  o = $.base.options
  #Activate the layout maker
  $.base.layout.activate()
  #Enable sidebar tree view controls
  $.base.tree '.sidebar'
  #Add slimscroll to navbar dropdown
  if o.navbarMenuSlimscroll and typeof $.fn.slimscroll != 'undefined'
    $('.navbar .menu').slimscroll(
      height: '200px'
      alwaysVisible: false
      size: '3px').css 'width', '100%'
  #Activate sidebar push menu
  if o.sidebarPushMenu
    $.base.pushMenu o.sidebarToggleSelector
  #Activate Bootstrap tooltip
  if o.enableBSToppltip
    $(o.BSTooltipSelector).tooltip()
  #Activate box widget
  if o.enableBoxWidget
    $.base.boxWidget.activate()
  #Activate fast click
  if o.enableFastclick and typeof FastClick != 'undefined'
    FastClick.attach document.body
  #Activate direct chat widget
  if o.directChat.enable
    $(o.directChat.contactToggleSelector).click ->
      box = $(this).parents('.direct-chat').first()
      box.toggleClass 'direct-chat-contacts-open'
      return

  ###
  # INITIALIZE BUTTON TOGGLE
  # ------------------------
  ###

  $('.btn-group[data-toggle="btn-toggle"]').each ->
    group = $(this)
    $(this).find('.btn').click (e) ->
      group.find('.btn.active').removeClass 'active'
      $(this).addClass 'active'
      e.preventDefault()
      return
    return
  return

### ----------------------
# - AdminLTE Functions -
# ----------------------
# All AdminLTE functions are implemented below.
###

### prepareLayout
# =============
# Fixes the layout height in case min-height fails.
#
# @type Object
# @usage $.base.layout.activate()
#        $.base.layout.fix()
#        $.base.layout.fixSidebar()
###

$.base.layout =
  activate: ->
    _this = this
    _this.fix()
    _this.fixSidebar()
    $(window, '.wrapper').resize ->
      _this.fix()
      _this.fixSidebar()
      return
    return
  fix: ->
    #Get window height and the wrapper height
    neg = $('.main-header').outerHeight() + $('.main-footer').outerHeight()
    window_height = $(window).height()
    sidebar_height = $('.sidebar').height()
    #Set the min-height of the content and sidebar based on the
    #the height of the document.
    if $('body').hasClass('fixed')
      $('.content-wrapper, .right-side').css 'min-height',
              window_height - $('.main-footer').outerHeight()
    else
      if window_height >= sidebar_height
        $('.content-wrapper, .right-side').css 'min-height', window_height - neg
      else
        $('.content-wrapper, .right-side').css 'min-height', sidebar_height
    return
  fixSidebar: ->
    #Make sure the body tag has the .fixed class
    if !$('body').hasClass('fixed')
      if typeof $.fn.slimScroll != 'undefined'
        $('.sidebar').slimScroll(destroy: true).height 'auto'
      return
    else if typeof $.fn.slimScroll == 'undefined' and console
      console.error 'Error: the fixed layout requires the slimscroll plugin!'
    #Enable slimscroll for fixed layout
    if $.base.options.sidebarSlimScroll
      if typeof $.fn.slimScroll != 'undefined'
        #Distroy if it exists
        $('.sidebar').slimScroll(destroy: true).height 'auto'
        #Add slimscroll
        $('.sidebar').slimscroll
          height: $(window).height() - $('.main-header').height() + 'px'
          color: 'rgba(0,0,0,0.2)'
          size: '3px'
    return

### PushMenu()
# ==========
# Adds the push menu functionality to the sidebar.
#
# @type Function
# @usage: $.base.pushMenu("[data-toggle='offcanvas']")
###

$.base.pushMenu = (toggleBtn) ->
  #Enable sidebar toggle
  $(toggleBtn).click (e) ->
    e.preventDefault()
    #Enable sidebar push menu
    $('body').toggleClass 'sidebar-collapse'
    $('body').toggleClass 'sidebar-open'
    return
  $('.content-wrapper').click ->
    #Enable hide menu when clicking on the
    # content-wrapper on small screens
    if $(window).width() <= 767 and $('body').hasClass('sidebar-open')
      $('body').removeClass 'sidebar-open'
    return
  return

### Tree()
# ======
# Converts the sidebar into a multilevel
# tree view menu.
#
# @type Function
# @Usage: $.base.tree('.sidebar')
###

$.base.tree = (menu) ->
  $('li a', $(menu)).click (e) ->
    #Get the clicked link and the next element
    $this = $(this)
    checkElement = $this.next()
    #Check if the next element is a menu and is visible
    if checkElement.is('.treeview-menu') and checkElement.is(':visible')
      #Close the menu
      checkElement.slideUp 'normal', ->
        checkElement.removeClass 'menu-open'
        return
      checkElement.parent('li').removeClass 'active'
    else if checkElement.is('.treeview-menu') and !checkElement.is(':visible')
      #Get the parent menu
      parent = $this.parents('ul').first()
      #Close all open menus within the parent
      ul = parent.find('ul:visible').slideUp('normal')
      #Remove the menu-open class from the parent
      ul.removeClass 'menu-open'
      #Get the parent li
      parent_li = $this.parent('li')
      #Open the target menu and add the menu-open class
      checkElement.slideDown 'normal', ->
        #Add the class active to the parent li
        checkElement.addClass 'menu-open'
        parent.find('li.active').removeClass 'active'
        parent_li.addClass 'active'
        return
    #if this isn't a link, prevent the page from being redirected
    if checkElement.is('.treeview-menu')
      e.preventDefault()
    return
  return

### BoxWidget
# =========
# BoxWidget is plugin to handle collapsing and
# removing boxes from the screen.
#
# @type Object
# @usage $.base.boxWidget.activate()
#								Set all of your option in the main $.base.options object
###

$.base.boxWidget =
  activate: ->
    o = $.base.options
    _this = this
    #Listen for collapse event triggers
    $(o.boxWidgetOptions.boxWidgetSelectors.collapse).click (e) ->
      e.preventDefault()
      _this.collapse $(this)
      return
    #Listen for remove event triggers
    $(o.boxWidgetOptions.boxWidgetSelectors.remove).click (e) ->
      e.preventDefault()
      _this.remove $(this)
      return
    return
  collapse: (element) ->
    #Find the box parent
    box = element.parents('.box').first()
    #Find the body and the footer
    bf = box.find('.box-body, .box-footer')
    if !box.hasClass('collapsed-box')
      #Convert minus into plus
      element.children('.fa-minus').removeClass('fa-minus').addClass 'fa-plus'
      bf.slideUp 300, ->
        box.addClass 'collapsed-box'
        return
    else
      #Convert plus into minus
      element.children('.fa-plus').removeClass('fa-plus').addClass 'fa-minus'
      bf.slideDown 300, ->
        box.removeClass 'collapsed-box'
        return
    return
  remove: (element) ->
    #Find the box parent
    box = element.parents('.box').first()
    box.slideUp()
    return
  options: $.base.options.boxWidgetOptions

### ------------------
# - Custom Plugins -
# ------------------
# All custom plugins are defined below.
###

###
# BOX REFRESH BUTTON
# ------------------
# This is a custom plugin to use with the compenet BOX. It allows you to add
# a refresh button to the box. It converts the box's state to a loading state.
#
#	@type plugin
# @usage $("#box-widget").boxRefresh( options );
###

(($) ->

  $.fn.boxRefresh = (options) ->
    # Render options
    settings = $.extend({
      trigger: '.refresh-btn'
      source: ''
      onLoadStart: (box) ->
      onLoadDone: (box) ->

    }, options)
    #The overlay
    overlay = $('<div class="overlay"></div><div class="loading-img"></div>')

    start = (box) ->
      #Add overlay and loading img
      box.append overlay
      settings.onLoadStart.call box
      return

    done = (box) ->
      #Remove overlay and loading img
      box.find(overlay).remove()
      settings.onLoadDone.call box
      return

    @each ->
      #if a source is specified
      if settings.source == ''
        if console
          console.log 'Please specify a source first - boxRefresh()'
        return
      #the box
      box = $(this)
      #the button
      rBtn = box.find(settings.trigger).first()
      #On trigger click
      rBtn.click (e) ->
        e.preventDefault()
        #Add loading overlay
        start box
        #Perform ajax call
        box.find('.box-body').load settings.source, ->
          done box
          return
        return
      return

  return
) jQuery

###
# TODO LIST CUSTOM PLUGIN
# -----------------------
# This plugin depends on iCheck plugin for checkbox and radio inputs
#
# @type plugin
# @usage $("#todo-widget").todolist( options );
###

(($) ->

  $.fn.todolist = (options) ->
    # Render options
    settings = $.extend({
      onCheck: (ele) ->
      onUncheck: (ele) ->

    }, options)
    @each ->
      if typeof $.fn.iCheck != 'undefined'
        $('input', this).on 'ifChecked', (event) ->
          ele = $(this).parents('li').first()
          ele.toggleClass 'done'
          settings.onCheck.call ele
          return
        $('input', this).on 'ifUnchecked', (event) ->
          ele = $(this).parents('li').first()
          ele.toggleClass 'done'
          settings.onUncheck.call ele
          return
      else
        $('input', this).on 'change', (event) ->
          ele = $(this).parents('li').first()
          ele.toggleClass 'done'
          settings.onCheck.call ele
          return
      return

  return
) jQuery

# ---
# generated by js2coffee 2.0.1
(($) ->
  
  $('a#modal-login-button').on 'click', (event) ->
    $('#signup-modal').modal 'toggle'
    return
 
  $('a#modal-signup-button').on 'click', (event) ->
    $('#login-modal').modal 'toggle'
    return
       
) jQuery
