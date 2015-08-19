'use strict'

app
    .controller('allActorsCtrl', function($http, $scope) {
    	$scope.actors= [];
        $http.get(HOSTED_URL + '/api/actor/').then(function  (response) {
        	$scope.actors = response.data;
        	console.log($scope.actors)
        } , function  (response) {
        	alert('Error Callback');
        	console.log("Error: ", response);
        })
    });
