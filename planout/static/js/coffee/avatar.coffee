'use strict'
if typeof jQuery == 'undefined'
  throw new Error('avatar js requires jQuery')
  
# ---
#
#
<<<<<<< HEAD
$upload_button = $('#submit-upload-avatar')
=======
>>>>>>> 678fbc60f0063e903f814ee87edee882027f0f1e

readURL = (input) ->
  if input.files and input.files[0]
    reader = new FileReader
    reader.onload = (e) ->
      $(".avatar-preview > img").attr 'src', e.target.result
      return
      
    reader.readAsDataURL input.files[0]
    return
<<<<<<< HEAD
    
CropAvatar = ($element) ->
  @$container = $element
  @$avatarPreview = $('div.avatar-preview-wrapper > a')
  ### this.$avatarView = this.$container.find('.avatar-view');
   this.$avatar = this.$avatarView.find('img');
  this.$avatarModal = this.$container.find('#avatar-modal');
  this.$loading = this.$container.find('.loading');
  ###
  @$avatarForm = @$container.find('form')
  @$avatarSubmit = $upload_button
  @$avatarData = @$avatarForm.find('.avatar-data')

  ### tthis.$avatarSrc = this.$avatarForm.find('.avatar-src');
  ###
  @$avatarInput = @$avatarForm.find('.avatar-input')
  @init()
  return

# CropAvatar.prototype =
#   constructor: CropAvatar
#   support:
#   fileList: ! !$('<input type="file">').prop('files')
#     blobURLs: ! !window.URL and URL.createObjectURL
#     formData: ! !window.FormData

#   init: ->
#     @support.
  
# #(($) ->
# #   imageData = undefined
# #   cropBoxData = undefined
# #   $("#avatarInput").change ->
# #     readURL this



CropAvatar.prototype =
  constructor: CropAvatar
  support:
    fileList: ! !$('<input type="file">').prop('files')
    blobURLs: ! !window.URL and URL.createObjectURL
    formData: ! !window.FormData
  init: ->
    @support.datauri = @support.fileList and @support.blobURLs
    @addListener()
    return
  addListener: ->
    @$avatarInput.on 'change', $.proxy(@change, this)
    @$avatarForm.on 'submit', $.proxy(@submit, this)
    @$avatarSubmit.on 'click', $.proxy(@submit, this)
    return
  click: ->
    return
  change: ->
    files = undefined
    file = undefined
    if @support.datauri
      files = @$avatarInput.prop('files')
      if files.length > 0
        file = files[0]
        if @isImageFile(file)
          if @url
            URL.revokeObjectURL @url
            # Revoke the old one
          @url = URL.createObjectURL(file)
          @startCropper()
    else
      file = @$avatarInput.val()
      if @isImageFile(file)
        @syncUpload()
    return
  submit: ->
    # if !@$avatarSrc.val() and !@$avatarInput.val()
    #   return false
    if !@$avatarInput.val()
      return false
    if @support.formData
      @ajaxUpload()
      return false
    return
  isImageFile: (file) ->
    if file.type
      /^image\/\w+$/.test file.type
    else
      /\.(jpg|jpeg|png|gif)$/.test file
  startCropper: ->
    _this = this
    console.log @url
    $upload_button.removeAttr 'disabled' # enable
    if @active
      @$img.cropper 'replace', @url
    else
      @$img = $('<img src="' + @url + '">')
      @$avatarPreview.empty().html @$img
      
      console.log @$avatarPreview.attr('class')
      @$img.cropper
        aspectRatio: 1
        # preview: @$avatarPreview.selector
        crop: (data) ->
          json = [
            '{"x":' + data.x
            '"y":' + data.y
            '"height":' + data.height
            '"width":' + data.width
            '"rotate":' + data.rotate + '}'
          ].join()
          _this.$avatarData.val json
          return
      @active = true
    return
  stopCropper: ->
    if @active
      @$img.cropper 'destroy'
      @$img.remove()
      @active = false
    return
  ajaxUpload: ->
    url = @$avatarForm.attr('action')
    data = new FormData(@$avatarForm[0])
    _this = this
    $.ajax url,
      type: 'post'
      data: data
      dataType: 'json'
      processData: false
      contentType: false
      beforeSend: ->
        _this.submitStart()
        return
      success: (data) ->
        _this.submitDone data
        return
      error: (XMLHttpRequest, textStatus, errorThrown) ->
        _this.submitFail textStatus or errorThrown
        return
      complete: ->
        _this.submitEnd()
        return
    return
  submitStart: ->
    # @$loading.fadeIn()
    return
  submitDone: (data) ->
    $upload_button.attr 'disabled', 'disabled'

    if $.isPlainObject(data) and data.state == 200
      if data.result
        @url = data.result
        if @support.datauri or @uploaded
          @uploaded = false
          @cropDone()
        else
          @uploaded = true
          @$avatarSrc.val @url
          @startCropper()
        @$avatarInput.val ''
      else if data.message
        @alert data.message
    else
      @alert 'Failed to response'
    return
  submitFail: (msg) ->
    @alert msg
    return
  submitEnd: ->
    # @$loading.fadeOut()
    return
  cropDone: ->
    @$avatarForm.get(0).reset()

    ###this.$avatar.attr('src', this.url);###

    @stopCropper()
    return
  alert: (msg) ->
    $alert = [
      '<div class="alert alert-danger avater-alert">'
      '<button type="button" class="close"
          data-dismiss="alert">&times;</button>'
      msg
      '</div>'
    ].join('')

    ###this.$avatarUpload.after($alert);###

    return

# ---
# generated by js2coffee 2.0.1

(($) ->
  $ ->
    $form_wrapper = $('.avatar-form-wrapper')
    if $form_wrapper.length
      new CropAvatar($form_wrapper)

  $(document).ready ->
    $upload_button.attr 'disabled', 'disabled'
    return
=======

(($) ->
  $("#avatarInput").change ->
    readURL this
  
>>>>>>> 678fbc60f0063e903f814ee87edee882027f0f1e
) jQuery



<<<<<<< HEAD

=======
>>>>>>> 678fbc60f0063e903f814ee87edee882027f0f1e
