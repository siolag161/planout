module.exports = (grunt) ->

  # Initial variable configuration 
  pkg = grunt.file.readJSON 'package.json'
  name = pkg.name.toLowerCase()
  path = "../" + name
  paths =
    templates: path + '/templates'
    css: path + '/static/css'
    scss: path + '/static/css/scss'
    fonts: path + '/static/fonts'
    img: path + '/static/img'
    js: path + '/static/js'
    coffee: path + '/static/js/coffee'
    config: path + '/config'
    tests: 'tests'
    vendors: './bower_components'

  # Loads grunt config automatically via broken up tasks
  # https://github.com/firstandthird/load-grunt-config
  require('load-grunt-config') grunt,
    data:
      name: name
      paths: paths
    loadGruntTasks:
      pattern: [
        'grunt-*'
        '!grunt-template-jasmine-istanbul'
      ]

  # Times how long tasks take
  # https://github.com/sindresorhus/time-grunt
  require('time-grunt') grunt
