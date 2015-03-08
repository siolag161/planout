(function() {
  'use strict';
  var $upload_button, CropAvatar, readURL;

  if (typeof jQuery === 'undefined') {
    throw new Error('avatar js requires jQuery');
  }

  $upload_button = $('#submit-upload-avatar');

  readURL = function(input) {
    var reader;
    if (input.files && input.files[0]) {
      reader = new FileReader;
      reader.onload = function(e) {
        $(".avatar-preview > img").attr('src', e.target.result);
      };
      reader.readAsDataURL(input.files[0]);
    }
  };

  CropAvatar = function($element) {
    this.$container = $element;
    this.$avatarPreview = $('div.avatar-preview-wrapper > a');

    /* this.$avatarView = this.$container.find('.avatar-view');
     this.$avatar = this.$avatarView.find('img');
    this.$avatarModal = this.$container.find('#avatar-modal');
    this.$loading = this.$container.find('.loading');
     */
    this.$avatarForm = this.$container.find('form');
    this.$avatarSubmit = $upload_button;
    this.$avatarData = this.$avatarForm.find('.avatar-data');

    /* tthis.$avatarSrc = this.$avatarForm.find('.avatar-src');
     */
    this.$avatarInput = this.$avatarForm.find('.avatar-input');
    this.init();
  };

  CropAvatar.prototype = {
    constructor: CropAvatar,
    support: {
      fileList: !!$('<input type="file">').prop('files'),
      blobURLs: !!window.URL && URL.createObjectURL,
      formData: !!window.FormData
    },
    init: function() {
      this.support.datauri = this.support.fileList && this.support.blobURLs;
      this.addListener();
    },
    addListener: function() {
      this.$avatarInput.on('change', $.proxy(this.change, this));
      this.$avatarForm.on('submit', $.proxy(this.submit, this));
      this.$avatarSubmit.on('click', $.proxy(this.submit, this));
    },
    click: function() {},
    change: function() {
      var file, files;
      files = void 0;
      file = void 0;
      if (this.support.datauri) {
        files = this.$avatarInput.prop('files');
        if (files.length > 0) {
          file = files[0];
          if (this.isImageFile(file)) {
            if (this.url) {
              URL.revokeObjectURL(this.url);
            }
            this.url = URL.createObjectURL(file);
            this.startCropper();
          }
        }
      } else {
        file = this.$avatarInput.val();
        if (this.isImageFile(file)) {
          this.syncUpload();
        }
      }
    },
    submit: function() {
      if (!this.$avatarInput.val()) {
        return false;
      }
      if (this.support.formData) {
        this.ajaxUpload();
        return false;
      }
    },
    isImageFile: function(file) {
      if (file.type) {
        return /^image\/\w+$/.test(file.type);
      } else {
        return /\.(jpg|jpeg|png|gif)$/.test(file);
      }
    },
    startCropper: function() {
      var _this;
      _this = this;
      console.log(this.url);
      $upload_button.removeAttr('disabled');
      if (this.active) {
        this.$img.cropper('replace', this.url);
      } else {
        this.$img = $('<img src="' + this.url + '">');
        this.$avatarPreview.empty().html(this.$img);
        console.log(this.$avatarPreview.attr('class'));
        this.$img.cropper({
          aspectRatio: 1,
          crop: function(data) {
            var json;
            json = ['{"x":' + data.x, '"y":' + data.y, '"height":' + data.height, '"width":' + data.width, '"rotate":' + data.rotate + '}'].join();
            _this.$avatarData.val(json);
          }
        });
        this.active = true;
      }
    },
    stopCropper: function() {
      if (this.active) {
        this.$img.cropper('destroy');
        this.$img.remove();
        this.active = false;
      }
    },
    ajaxUpload: function() {
      var data, url, _this;
      url = this.$avatarForm.attr('action');
      data = new FormData(this.$avatarForm[0]);
      _this = this;
      $.ajax(url, {
        type: 'post',
        data: data,
        dataType: 'json',
        processData: false,
        contentType: false,
        beforeSend: function() {
          _this.submitStart();
        },
        success: function(data) {
          _this.submitDone(data);
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
          _this.submitFail(textStatus || errorThrown);
        },
        complete: function() {
          _this.submitEnd();
        }
      });
    },
    submitStart: function() {},
    submitDone: function(data) {
      $upload_button.attr('disabled', 'disabled');
      if ($.isPlainObject(data) && data.state === 200) {
        if (data.result) {
          this.url = data.result;
          if (this.support.datauri || this.uploaded) {
            this.uploaded = false;
            this.cropDone();
          } else {
            this.uploaded = true;
            this.$avatarSrc.val(this.url);
            this.startCropper();
          }
          this.$avatarInput.val('');
        } else if (data.message) {
          this.alert(data.message);
        }
      } else {
        this.alert('Failed to response');
      }
    },
    submitFail: function(msg) {
      this.alert(msg);
    },
    submitEnd: function() {},
    cropDone: function() {
      this.$avatarForm.get(0).reset();

      /*this.$avatar.attr('src', this.url); */
      this.stopCropper();
    },
    alert: function(msg) {
      var $alert;
      $alert = ['<div class="alert alert-danger avater-alert">', '<button type="button" class="close" data-dismiss="alert">&times;</button>', msg, '</div>'].join('');

      /*this.$avatarUpload.after($alert); */
    }
  };

  (function($) {
    $(function() {
      var $form_wrapper;
      $form_wrapper = $('.avatar-form-wrapper');
      if ($form_wrapper.length) {
        return new CropAvatar($form_wrapper);
      }
    });
    return $(document).ready(function() {
      $upload_button.attr('disabled', 'disabled');
    });
  })(jQuery);

}).call(this);

//# sourceMappingURL=avatar.js.map
