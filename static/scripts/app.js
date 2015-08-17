'use strict';

/**
 * @ngdoc overview
 * @name crowdCastingApp
 * @description
 * # crowdCastingApp
 *
 * Main module of the application.
 */
var app = angular
  .module('crowdCastingApp', [
    'ngAria',
    'ngCookies',
    'ngMessages',
    'ngResource',
    'ngSanitize',
    'ngTouch',
    'ui.router'
      ]);

app.config(function($stateProvider, $urlRouterProvider) {
  //
  // For any unmatched url, redirect to /state1
  $urlRouterProvider.otherwise("/");
  //
  // Now set up the states
  $stateProvider
    .state('home', {
      url: "/home",
      templateUrl: "/static/views/main.html"
    })
});