'use strict';

app
    .controller('profileCtrl', ['$scope', '$http', '$stateParams', '$location', '$cookies', function($scope, $http, $stateParams, $location, $cookies) {
        $scope.charactristics = true;
        $scope.experiences = false;
        $scope.tags = false;
        $scope.actor;
        $scope.dynamicPopover = {
            templateUrl: 'views/picture-edit.html'
        };
        $scope.style = {
            'padding-left': '10px'
        }

        $http.get(HOSTED_URL + '/api/actor/' + $stateParams.id + '/').then(function(response) {
            $scope.actor = response.data;
            if ($scope.actor.profile_picture)
                $scope.img = $scope.actor.profile_picture;
            else
                $scope.img = 'images/yeoman.png';
        }, function(response) {
            alert("ERROR");
            console.log('ERROR response: ', response);
        });
        $scope.readURL = function(input) {

            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.onload = function(e) {
                    $scope.img = e.target.result;
                    $('#img').attr('src', $scope.img);
                    $scope.actor.profile_picture = $scope.img;
                    $http.get(HOSTED_URL + '/csrf/token/').then(function(response) {

                        // CSRF TOKEN
                        $cookies.put('csrftoken', response.data.csrf);
                        console.log('CSRF Success', response.data.csrf);
                        $http.defaults.headers.post['X-CSRFToken'] = response.data.csrf;
                        $http.defaults.headers.put['X-CSRFToken'] = response.data.csrf;


                        $http.put(HOSTED_URL + '/api/actor/' + $stateParams.id + '/', $scope.actor).success(function() {
                            console.log('peeep');
                        });
                    }, function(response) {
                        console.log('CSRF FAILED: ', response);
                    })
                }
                reader.readAsDataURL(input.files[0]);
            }
        }

        $('#img-upload').on('change', function(event) {
            $scope.readURL(this);
        });
        $scope.submitInfo = function(actor) {
            $scope.editing = false

            $http.get(HOSTED_URL + '/csrf/token/').then(function(response) {

                // CSRF TOKEN
                $cookies.put('csrftoken', response.data.csrf);
                console.log('CSRF Success', response.data.csrf);
                $http.defaults.headers.post['X-CSRFToken'] = response.data.csrf;
                $http.defaults.headers.put['X-CSRFToken'] = response.data.csrf;
                // $http.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';



                // $http.defaults.headers.post['csrf'] = $cookies.get('csrftoken');



                $http.put(HOSTED_URL + '/api/actor/' + $stateParams.id + '/', actor).success(function() {
                    console.log('peeep');
                });

            }, function(response) {
                console.log('CSRF FAILED: ', response);
            })
        }
        $scope.animate = function() {
            if ($scope.charactristics) {
                $scope.charactristics = false
                $scope.experiences = true
                $('.picture').addClass('picture-exp');
            } else {
                if ($scope.tags) {
                    $scope.tags = false
                    $scope.charactristics = true
                    $('.picture').removeClass('picture-tag');
                } else {
                    if ($scope.experiences) {
                        $scope.experiences = false
                        $scope.tags = true
                        $('.picture').removeClass('picture-exp');
                        $('.picture').addClass('picture-tag');
                    }
                }
            }
        }

    }]);
