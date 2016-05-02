'use strict';
var gulp = require('gulp');
var del = require('del');
var gutil = require('gulp-util');

// BrowserSync
var browserSync = require('browser-sync');

// js
var watchify = require('watchify');
var browserify = require('browserify');

// --------------------------
// CUSTOM TASK METHODS
// --------------------------
var tasks = {
  // --------------------------
  // Delete build folder
  // --------------------------
    clean: function(cb) {
    del(['build/'], cb);
  },
  // --------------------------
  // Copy static assets
  // --------------------------
  assets: function() {
    return gulp.src('./static/**/*')
      .pipe(gulp.dest('build/static/'));
  },

  // --------------------------
  // HTML
  // --------------------------
  // html templates (when using the connect server)
  templates: function() {
    gulp.src('templates/*.html')
      .pipe(gulp.dest('build/'));
  },
  // --------------------------
  // Browserify
  // --------------------------
  browserify: function() {
    var bundler = browserify('./static/js/index.js', {
      debug: !production,
      cache: {}
    });

    if (watch) {
      bundler = watchify(bundler);
    }
    var rebundle = function() {
      return bundler.bundle()
        .on('error', handleError('Browserify'))
        .pipe(source('build.js'))
        .pipe(gulp.dest('build/js/'));
    };
    bundler.on('update', rebundle);
    return rebundle();
  },

};

gulp.task('browser-sync', function() {
    browserSync({
        server: {
            baseDir: "./build"
        },
        port: process.env.PORT || 3000
    });
});

gulp.task('reload-js', ['browserify'], function(){
  browserSync.reload();
});
gulp.task('reload-templates', ['templates'], function(){
  browserSync.reload();
});

// --------------------------
// CUSTOMS TASKS
// --------------------------
gulp.task('templates', tasks.templates);
gulp.task('assets', tasks.assets);
gulp.task('browserify', tasks.browserify);

// --------------------------
// DEV/WATCH TASK
// --------------------------
// gulp.task('watch', ['assets', 'templates', 'sass', 'browserify', 'browser-sync'], function() {
gulp.task('watch', ['browser-sync'], function() {

  // --------------------------
  // watch:sass
  // --------------------------
  gulp.watch('./static/scss/**/*.scss', ['reload-sass']);

  // --------------------------
  // watch:js
  // --------------------------
  gulp.watch('./static/js/**/*.js', ['lint:js', 'reload-js']);

  // --------------------------
  // watch:html
  // --------------------------
  gulp.watch('./templates/**/*.html', ['reload-templates']);

  gutil.log(gutil.colors.bgGreen('Watching for changes...'));
});

// build task
gulp.task('build', [
  'clean',
  'templates',
  'assets',
  'browserify'
]);

gulp.task('default', ['watch']);
