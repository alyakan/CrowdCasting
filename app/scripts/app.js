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
        'ui.router',
        'ui.bootstrap',
        'flow'
    ]);

var HOSTED_URL = "http://localhost:8000";

app.config(function($stateProvider, $urlRouterProvider, $httpProvider) {
    // Common configuration for django to be abl to use is_ajax
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.withCredentials = true;
    $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
    $httpProvider.defaults.transformRequest = [function(data) {
        return angular.isObject(data) && String(data) !== '[object File]' ? param(data) : data;
    }];

    // ROUTES
    $urlRouterProvider.otherwise("/");
    $stateProvider
        .state('actors', {
            url: "/actor",
            templateUrl: "views/all_actors.html",
            controller: "allActorsCtrl"
        })
        .state('profile', {
            url: "/profile/:id",
            templateUrl: "views/profile.html",
            controller: "profileCtrl"
        })
        .state('actor-detail', {
            url: "/actor/:id",
            templateUrl: "views/detail_actors.html",
            controller: "actorCtrl"
        })
        .state('index', {
            url: "/",
            templateUrl: "views/main.html",
            controller: "MainCtrl"
        })
        .state('signin', {
            url: "/signin",
            templateUrl: "views/signin.html",
            controller: "SigninCtrl"
        })
        .state('signup', {
            url: "/signup",
            templateUrl: "views/signup.html",
            controller: "SignupCtrl"
        })
        .state('search', {
            url: "/search",
            templateUrl: "views/search.html"
        })


}).run(function($http, $cookies) {

    // GET REQUEST FOR CSRF TOKEN TO BE USED THROUGHT THE APP
    $http.get(HOSTED_URL + '/csrf/token/').then(function(response) {
        $cookies.put('csrftoken', response.data.csrf);
        console.log('CSRF Success', response.data.csrf);

        // CSRF TOKEN
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.get('csrftoken');
        // $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';



        // $http.defaults.headers.post['csrf'] = $cookies.get('csrftoken');



        // TO BE REMOVED WHEN SIGIN IS DONE
        $http.post(HOSTED_URL + '/api-auth/login/', {
            username: 'director',
            password: 'test',
            next: 'api/user/'
        }).then(function(response) {}, function(response) {})


    }, function(response) {
        console.log('CSRF FAILED: ', response);
    })
})

// $http.defaults.headers.post['csrf'] = $cookies.get('csrftoken');



// // TO BE REMOVED WHEN SIGIN IS DONE
// $http.post(HOSTED_URL + '/api-auth/login/', {
//     username: 'test',
//     password: 'test',
//     next: 'api/user/'
// }).then(function(response) {
//     console.log('Signin Success: ', response);
// }, function(response) {
//     console.log('Signin Error: ', response);
// });




/**
 * The workhorse; converts an object to x-www-form-urlencoded serialization.
 * @param {Object} obj
 * @return {String}
 */
var param = function(obj) {
    var query = '',
        name, value, fullSubName, subName, subValue, innerObj, i;

    for (name in obj) {
        value = obj[name];

        if (value instanceof Array) {
            for (i = 0; i < value.length; ++i) {
                subValue = value[i];
                fullSubName = name + '[' + i + ']';
                innerObj = {};
                innerObj[fullSubName] = subValue;
                query += param(innerObj) + '&';
            }
        } else if (value instanceof Object) {
            for (subName in value) {
                subValue = value[subName];
                fullSubName = name + '[' + subName + ']';
                innerObj = {};
                innerObj[fullSubName] = subValue;
                query += param(innerObj) + '&';
            }
        } else if (value !== undefined && value !== null)
            query += encodeURIComponent(name) + '=' + encodeURIComponent(value) + '&';
    }

    return query.length ? query.substr(0, query.length - 1) : query;
};
