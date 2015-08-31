'use strict'

app.controller('SigninCtrl', function($http,$scope,$cookies) {
            $scope.username;
            $scope.password;
            $scope.login = function() {
                $http.get(HOSTED_URL + '/csrf/token/').then(function(response) {

                    // CSRF TOKEN
                    $cookies.put('csrftoken', response.data.csrf);
                    console.log('CSRF Success', response.data.csrf);
                    $http.defaults.headers.post['X-CSRFToken'] = response.data.csrf;
                    $http.defaults.headers.put['X-CSRFToken'] = response.data.csrf;


                    $http.post(HOSTED_URL + '/api-auth/login/', {
                        username: $scope.username,
                        password: $scope.password,
                        next: 'api/user/'
                    }).then(function(response) {}, function(response) {});

                }, function(response) {
                    console.log('CSRF FAILED: ', response);
                });
}
});