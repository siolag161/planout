module.exports =

  # Copy files and folders
  # https://github.com/gruntjs/grunt-contrib-copy

  jasmine:
    expand: true
    flatten: true
    src: '<%= paths.js %>/tests/lib/*.js'
    dest: '<%= paths.js %>/tests/build/'

  coverage:
    src: '<%= paths.tests %>/jasmine/index.html'
    dest: '<%= paths.tests %>/jasmine/coverage.html'

  specRunner:
    src: '_SpecRunner.html'
    dest: '<%= paths.tests %>/jasmine/index.html'
 
  font_bower:
    expand: true
    flatten: true
    src: '<%= paths.vendors %>/*/fonts/*'
    dest: '<%= paths.css %>/fonts'
