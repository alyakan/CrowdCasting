'use strict'


app.controller('SignupCtrl', function($http, $scope, $stateParams, $location) {
    $scope.email;
    $scope.password;
    $scope.username;
    $scope.passwordconfirm;
    $scope.password;
    $scope.last_name;
    $scope.first_name;
    $scope.signup = function() {
    	if ($scope.passwordconfirm === $scope.password){
        $http.get(HOSTED_URL + '/csrf/token/').then(function(response) {

            // CSRF TOKEN
            $cookies.put('csrftoken', response.data.csrf);
            console.log('CSRF Success', response.data.csrf);
            $http.defaults.headers.post['X-CSRFToken'] = response.data.csrf;
            $http.defaults.headers.put['X-CSRFToken'] = response.data.csrf;


            $http.post(HOSTED_URL + '/api/'+$scope.role+'/', {
                username: $scope.username,
                first_name: $scope.first_name,
                last_name: $scope.last_name,
                email:$scope.email,
                password: $scope.password
            }).then(function(response) {}, function(response) {});

        }, function(response) {
            console.log('CSRF FAILED: ', response);
        });
    }
    else {
    	alert("passwords don't match");
    }
}
})
