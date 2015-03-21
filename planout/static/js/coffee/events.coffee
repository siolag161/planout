'use strict'
if typeof jQuery == 'undefined'
  throw new Error('avatar js requires jQuery')

class SplitDateTime
  constructor: ($element) ->
    @$container = $element
    @$dateInput = @$container.find('.input-group.date')
    @$timeInput = @$container.find('.input-group.time')
    @dateOpts =
      format: 'dd/mm/yyyy'
      autoclose: true
    @timeOpts =
      default: 'now'
      autoclose: true
      minutestep: 5
      twelvehour: true
    @init()
    
  init: ->
    @addListener()
    
  addListener: ->
    @datePicker = @$dateInput.datepicker(@dateOpts)
      .on 'changeDate', $.proxy(@dateChange, @)
    @timePicker = @$timeInput.clockpicker(@timeOpts)
      
  dateChange: (e) ->
    console.log("dateChanged")
    e.preventDefault()
    @$timeInput.clockpicker().clockpicker('show')
    return
    
EventPush = ($element) ->
  @$container = $element
  @$locationPreview = $('#location-map-preview')
  @$formSubmit = $('#event-form-submit')
  @$locationInput = $('#id_location')

  @$event_form = @$container.find('form')

  @$startSplit = new SplitDateTime(@$container.find('#div_id_start_time'))
  @$endSplit = new SplitDateTime(@$container.find('#div_id_end_time'))

  '''
  timing setup
  '''
  @$timeOpts =
    default: 'now'
    autoclose: true
    minutestep: 5
    twelvehour: true
  '''
  location setup
  '''
  @$location_fields = @$event_form.find(".superlocation input")
  @$superloc_input =  @$event_form.find("#div_id_location")
  @$superloc_field = @$event_form.find("#id_location")
  @$hid_toggle_fields = @$event_form.find(".toggle-field.hid")

  @$locResetButton = @$container.find('.location-reset')
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

    
    @$locResetButton.on 'click', $.proxy(@resetLocation, @)
    return

  resetLocationData: ->
    #console.log(@$locationInput.val())
    @$location_fields.val("")
    @$superloc_field.val("")
    return

  hideLocationFields: ->
    @$superloc_input.show "fast"
    @$hid_toggle_fields.hide "fast"
    @$mapCanvasWrapper.addClass('hidden')
    
    return

  resetLocation: (e)->
    @hideLocationFields()
    e.preventDefault()
    @resetLocationData()
    return
    
  submit: (event) ->
    return
    
  locationChange: (event, result) -> # fat arrow for proxy this
    @$superloc_input.hide "fast"
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
