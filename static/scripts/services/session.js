'use strict';

/**
 * @ngdoc service
 * @name crowdCastingApp.Session
 * @description
 * # Session
 * Service in the crowdCastingApp.
 */

angular.module('crowdCastingApp')
  .factory('Session', function ($resource) {
    return $resource('/api-auth/');
  });