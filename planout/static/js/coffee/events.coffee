'use strict'
if typeof jQuery == 'undefined'
  throw new Error('avatar js requires jQuery')


(($) ->
  $(".input-group.date").datepicker
    format: 'dd/mm/yyyy'
    autoclose: true
    pickerPosition: 'auto'
    startDate: '+0d'
    showMeridian: true
  $(".input-group.time").clockpicker
    default: 'now'
    autoclose: true
    minutestep: 5
    twelvehour: true
) jQuery

EventPush = ($element) ->
  @$container = $element
  @$locationPreview = $('#location-map-preview')
  @$formSubmit = $('#event-form-submit')
  @$locationInput = $('#id_location')

  @$event_form = @$container.find('form')

  @$location_fields = @$event_form.find("input[type=text].superlocation")
  @$hid_toggle_fields = @$event_form.find(".toggle-field.hid")

  @$resetBtn = @$container.find('.location-reset')
  @$mapCanvasWrapper = @$container.find('#google_map_canvas_wrapper')

  @$map = undefined
    
  @init()
  return

EventPush.prototype =
  constructor: EventPush
  init: ->
    @addListener()
    return
  addListener: ->
    @$locationInput.geocomplete(
      map: ".map_canvas"
      details: '.superlocation'
      detailsAttribute: "data-geo"
      types: ["geocode", "establishment"]
      componentRestrictions: country: 'vn'
    ).on 'geocode:result', $.proxy(@locationChange, @)
    
    @$resetBtn.on 'click', $.proxy(@resetLocation, @)
    return

  resetLocationData: ->
    #console.log(@$locationInput.val())
    @$location_fields.val("")
    return

  hideLocationFields: ->
    @$hid_toggle_fields.hide "fast"
    @$mapCanvasWrapper.addClass('hidden')

    return

  resetLocation: ->
    @hideLocationFields()
    @resetLocationData()
    return
    
  submit: (event) ->
    return
    
  locationChange: (event, result) -> # fat arrow for proxy this
  
    @$hid_toggle_fields.show "fast"
    @$mapCanvasWrapper.removeClass('hidden')
    if not @$map
      @$map = @$locationInput.geocomplete("map")

    google.maps.event.trigger @$map, 'resize'
    
    return
  ensureTime: ->
    return
  

(($) ->
  $(document).ready ->
    $form_wrapper = $('#event_form_wrapper')
    if $form_wrapper.length
      new EventPush($form_wrapper)
    return
) jQuery
