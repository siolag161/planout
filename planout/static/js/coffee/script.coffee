'use strict'
if typeof jQuery == 'undefined'
  throw new Error('avatar js requires jQuery')
  
(($) ->
  $(".input-group.date").datetimepicker
    format: 'dd/mm/yyyy hh:ii'
    autoclose: true
<<<<<<< HEAD
    pickerPosition: 'top-left'
    startDate: '+0d'
    showMeridian: true
=======
    pickerPosition: 'bottom-left'
    startDate: '+0d'
    showMeridian: true
    
>>>>>>> 678fbc60f0063e903f814ee87edee882027f0f1e
) jQuery

$(document).ready ->
  $('ul.nav li.dropdown').hover (->
    $(this).find('.dropdown-menu').stop(true, true).delay(100).fadeIn 300
    return
  ), ->
    $(this).find('.dropdown-menu').stop(true, true).delay(100).fadeOut 300
    return
      
  return
