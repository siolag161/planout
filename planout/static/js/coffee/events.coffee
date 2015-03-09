'use strict'
if typeof jQuery == 'undefined'
  throw new Error('avatar js requires jQuery')

EventPush = ($element) ->
  @$container = $element
  @$locationPreview = $('#location-map-preview')
  @$formSubmit = $('#event-form-submit')
  @$locationInput = $('#id_location')
  @init()
  return

EventPush.prototype =
  constructor: EventPush
  init: ->
    @addListener()
    return
  addListener: ->
    # @$locationInput.on 'change', $.proxy(@locationChange, this)
    @$locationInput.geocomplete(
      details: '#superlocation'
      detailsAttribute: "data-geo"
    ).on 'geocode:result',
      $.proxy(@locationChange, this)

    # ).bind('geocode:error', (event, status) ->
    #   console.log 'ERROR: ' + status
    #   return
    # ).bind 'geocode:multiple', (event, results) ->
    #   console.log 'Multiple: ' + results.length + ' results found'
    #   return
    return
  submit: ->
    return
  locationChange: (event, result)->
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
