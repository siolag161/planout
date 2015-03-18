'use strict'
if typeof jQuery == 'undefined'
  throw new Error('avatar js requires jQuery')
  

$(document).ready ->
  $('ul.nav li.dropdown').hover (->
    $(this).find('.dropdown-menu').stop(true, true).delay(100).fadeIn 300
    return
  ), ->
    $(this).find('.dropdown-menu').stop(true, true).delay(100).fadeOut 300
    return
      
  return
