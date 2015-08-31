'use strict'

app.controller('SigninCtrl', function($http, $scope, $stateParams, $location) {
	$scope.email;
	$scope.password;
	        $scope.login = function(){
	        $http.post(HOSTED_URL + '/api-auth/login/', {
            email: $scope.email,
            password: $scope.password,
            next: 'api/actor/'
        }).then(function(response) {
        	console.log('CSRF FAILED: ', response);
        }, function(response) {})
};
})