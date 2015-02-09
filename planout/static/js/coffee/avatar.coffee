((factory) ->
  if typeof define == 'function' and define.amd
    define [ 'jquery' ], factory
  else
    factory jQuery
  return
) ($) ->

  CropAvatar = ($element) ->
    @$container = $element
    @$avatarSubmit = @$container.find('#avatar-form-submit')
    @$avatarView = @$container.find('.avatar-view')
    @$avatar = @$avatarView.find('img')
    @$avatarModal = @$container.find('#avatar-modal')
    @$loading = @$container.find('.loading')
    @$avatarForm = @$avatarModal.find('.avatar-form')
    @$avatarUpload = @$avatarForm.find('.avatar-upload')
    @$avatarSrc = @$avatarForm.find('.avatar-src')
    @$avatarData = @$avatarForm.find('.avatar-data')
    @$avatarInput = @$avatarForm.find('.avatar-input')
    @$avatarSave = @$avatarForm.find('.avatar-save')
    @$avatarWrapper = @$avatarModal.find('.avatar-wrapper')
    @$avatarPreview = @$avatarModal.find('.avatar-preview')
    @init()
    console.log this
    return

  'use strict'
  console = window.console or log: $.noop
  CropAvatar.prototype =
    constructor: CropAvatar
    support:
      fileList: !!$('<input type="file">').prop('files')
      fileReader: !!window.FileReader
      formData: !!window.FormData
    init: ->
      @support.datauri = @support.fileList and @support.fileReader
      if !@support.formData
        @initIframe()
      @initTooltip()
      @initModal()
      @addListener()
      return
    addListener: ->
      @$avatarInput.on 'change', $.proxy(@change, this)
      @$avatarSubmit.on 'click', $.proxy(@submit, this)
      @$avatarForm.on 'submit', $.proxy(@submit, this)
      return
    initTooltip: ->
      @$avatarView.tooltip placement: 'bottom'
      return
    initModal: ->
      # @$avatarModal.modal 'hide'
      @initPreview()
      return
    initPreview: ->
      url = @$avatar.attr('src')
      @$avatarPreview.empty().html '<img src="' + url + '">'
      return
    initIframe: ->
      iframeName = 'avatar-iframe-' + Math.random().toString().replace('.', '')
      $iframe = $('<iframe name="' + iframeName \
                + '" style="display:none;"></iframe>')
      firstLoad = true
      _this = this
      @$iframe = $iframe
      @$avatarForm.attr('target', iframeName).after $iframe
      @$iframe.on 'load', ->
        data = undefined
        win = undefined
        doc = undefined
        try
          win = @contentWindow
          doc = @contentDocument
          doc = if doc then doc else win.document
          data = if doc then doc.body.innerText else null
        catch e
        if data
          _this.submitDone data
        else
          if firstLoad
            firstLoad = false
          else
            _this.submitFail 'Image upload failed!'
        _this.submitEnd()
        return
      return
    change: ->
      files = undefined
      file = undefined
      if @support.datauri
        files = @$avatarInput.prop('files')
        if files.length > 0
          file = files[0]
          if @isImageFile(file)
            @read file
      else
        file = @$avatarInput.val()
        if @isImageFile(file)
          @syncUpload()
      return
    submit: ->
      if !@$avatarSrc.val() and !@$avatarInput.val()
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
    read: (file) ->
      _this = this
      fileReader = new FileReader
      fileReader.readAsDataURL file

      fileReader.onload = ->
        _this.url = @result
        _this.startCropper()
        return

      return
    startCropper: ->
      _this = this
      if @active
        @$img.cropper 'replace', @url
      else
        @$img = $('<img src="' + @url + '">')
        @$avatarWrapper.empty().html @$img
        @$img.cropper
          aspectRatio: 1
          preview: @$avatarPreview.selector
          done: (data) ->
            json = [
              '{"x":' + data.x
              '"y":' + data.y
              '"height":' + data.height
              '"width":' + data.width + '}'
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
    syncUpload: ->
      @$avatarSave.click()
      return
    submitStart: ->
      @$loading.fadeIn()
      return
    submitDone: (data) ->
      console.log data
      try
        data = $.parseJSON(data)
      catch e
      if data and data.state == 200
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
      @$loading.fadeOut()
      return
    cropDone: ->
      @$avatarSrc.val ''
      @$avatarData.val ''
      @$avatar.attr 'src', @url
      @stopCropper()
      @$avatarModal.modal 'hide'
      return
    alert: (msg) ->
      $alert = [
        '<div class="alert alert-danger avater-alert">'
        '<button type="button" class="close"\
                   data-dismiss="alert">&times;</button>'
        msg
        '</div>'
      ].join('')
      @$avatarUpload.after $alert
      return
  $ ->
    example = new CropAvatar($('#crop-avatar'))
    return
  return

# ---
# generated by js2coffee 2.0.0
