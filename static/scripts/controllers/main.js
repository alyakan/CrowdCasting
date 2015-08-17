'use strict';

/**
 * @ngdoc function
 * @name crowdCastingApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the crowdCastingApp
 */
angular.module('crowdCastingApp')
  .controller('MainCtrl', function ($http) {
    this.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];

    $http.get("http://localhost:8000/request_account/").success(function  (response) {
    	console.log('Success response: ', response);
    }).error(function(response) {
    	console.log('Error response: ', response);
    });
  });
