'use strict'

app
    .controller('allActorsCtrl', function($http) {

        $http.get('http://localhost:8000/api/actor/').then(function  (response) {
        	alert('success Callback');
        	console.log("SUCCESS: ", response);
        } , function  (response) {
        	alert('Error Callback');
        	console.log("Error: ", response);
        })
    });
