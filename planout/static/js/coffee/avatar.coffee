'use strict'
if typeof jQuery == 'undefined'
  throw new Error('avatar js requires jQuery')
  
# ---
#
#

readURL = (input) ->
  if input.files and input.files[0]
    reader = new FileReader
    reader.onload = (e) ->
      $(".avatar-preview > img").attr 'src', e.target.result
      return
      
    reader.readAsDataURL input.files[0]
    return

(($) ->
  $("#avatarInput").change ->
    readURL this
  
) jQuery



