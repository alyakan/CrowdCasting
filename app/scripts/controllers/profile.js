'use strict';

app
    .controller('profileCtrl', ['$scope', function($scope) {
        $scope.dynamicPopover = {
            templateUrl: 'views/picture-edit.html'
        };
        $scope.img = "images/yeoman.png";
        $scope.details = {
            "name": 'menna',
            "age": '23',
            "experiences": {
                'a': 'a',
                'b': 'b',
                'c': 'c'
            },
            "bio": 'lorem',
            "contact_info": '487828578'
        };
        $scope.readURL = function(input) {

            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.onload = function(e) {
                    $scope.img = e.target.result;
                    $('#img').attr('src', $scope.img);
                }
                reader.readAsDataURL(input.files[0]);
            }
        }

        $('#img-upload').on('change', function(event) {
            $scope.readURL(this);
        })

    }]);
