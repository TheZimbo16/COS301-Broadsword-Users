var myApp = angular.module('myApp', []);
myApp.controller('AppCtrl', ['$scope', '$http', function($scope, $http) {
    console.log("Hello World from controller");
	var refresh = function(){
	$http.get('/userDB').then(doneCallbacks, failCallbacks);
	$scope.user = null;
};
refresh();
	$scope.addUser = function(){
		console.log($scope.user);
		$http.post('/userDB',$scope.user).then(function(response){
			console.log(response);
			refresh();
		});
		
	}
	$scope.remove = function(id){
		console.log(id);
		$http.delete('/userDB/'+id).then(function(response){
			refresh();
		});
	};
    $scope.edit = function(id){
		console.log(id);
		$http.get('/userDB/'+id).then(function(response){
			$scope.user = response.data;
		 });
	 };

	 $scope.update = function(){
	 	console.log($scope.user._id);
	 	$http.put('/userDB/' + $scope.user._id, $scope.user).then(function(response){
	 		refresh();
	 	});
	 };
	
	 $scope.deselect = function(){
	 	$scope.user = null;
	 }

	 function doneCallbacks(res) {
	  console.log("Data received");
	  $scope.userDB = res.data;
	 };

	 function failCallbacks(err) {
	 	 console.log(err.message);
	 };

	 


}]);﻿