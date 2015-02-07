 module.exports =
  # retrives and concats bower packages into dest directory
  # https://github.com/sapegin/grunt-bower-concat
  
  basic: 
    dest: '<%= paths.js %>/lib/vendors.js'
    cssDest:  '<%= paths.css %>/lib/vendors.css'
    dependencies:  
      'bootstrap': 'jquery'
      'underscore': 'jquery'
    exclude: [
      'jasmine'
      'jasmine-ajax'
      'jasmine-jquery']
  test: 
    dest: '<%= paths.js %>/tests/lib/vendors_test.js'
    include: [
      'jasmine-ajax'
      'jasmine-jquery']
    
      
