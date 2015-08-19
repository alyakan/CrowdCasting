'use strict'


app.controller('actorCtrl', function($http, $scope, $stateParams, $location) {
	console.log($stateParams.id);
	$scope.actor;
	$http.get(HOSTED_URL + '/api/actor/' + $stateParams.id + '/').then(function  (response) {
		$scope.actor = response.data;
	}, function  (response) {
		alert("ERROR");
		console.log('ERROR response: ', response);
	}) 
})
