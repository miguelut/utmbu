module.exports = function(grunt) {

  grunt.initConfig({
    jshint: {
      files: ['Gruntfile.js','static/**/*.js','test/**/*.js', '!**/lib/*'],
      options: {
        globals: {
          jQuery: true,
        }
      }
    },
    browserSync:{
      bsFiles: ['<%= watch.files %>'],
      options:{
        server:{
          baseDir: './'
        }
      }
    },
    watch: {
      files: ['<%= jshint.files %>', 'static/**/*.css'],
      tasks: ['jshint']
    }
  });

  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-browser-sync');

  grunt.registerTask('default', ['jshint', 'watch', 'browserSync']);

};
