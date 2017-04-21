var myApp = angular.module('myApp', []);
myApp.directive('fileModel', ['$parse', function ($parse) {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {
            var model = $parse(attrs.fileModel);
            var modelSetter = model.assign;

            element.bind('change', function () {
                scope.$apply(function () {
                    modelSetter(scope, element[0].files[0]);
                });
            });
        }
    };
}]);

myApp.service('fileUpload', ['$http', function ($http) {
    this.uploadFileToUrl = function (file, uploadUrl) {
        var fd = new FormData();
        fd.append('file', file);

        $http.post(uploadUrl, fd, {
                transformRequest: angular.identity,
                headers: {'Content-Type': undefined}
            })

            .then(function () {
                document.location.reload();
            })
    }
}]);

myApp.controller('MyCtrl', ['$scope', 'fileUpload', function ($scope, fileUpload) {
    $scope.uploadFile = function () {
        var file = $scope.myFile;
        document.location.reload();
        console.log('file is ');
        console.dir(file);

        var uploadUrl = "/upload";
        fileUpload.uploadFileToUrl(file, uploadUrl);
    };
    $scope.uploadFile1 = function () {
        var file = $scope.myFile;
        document.location.reload();
        console.log('file is ');
        console.dir(file);

        var uploadUrl = "/upload1";
        fileUpload.uploadFileToUrl(file, uploadUrl);
    };
    $scope.uploadFile2 = function () {
        var file = $scope.myFile;
        document.location.reload();
        console.log('file is ');
        console.dir(file);

        var uploadUrl = "/upload2";
        fileUpload.uploadFileToUrl(file, uploadUrl);
    };
    $scope.uploadcsv1 = function () {
        var file = $scope.myFile;
        document.location.reload();
        console.log('file is ');
        console.dir(file);

        var uploadUrl = "/uploadCsv1";
        fileUpload.uploadFileToUrl(file, uploadUrl);
    };
	$scope.uploadcsv2 = function () {
        var file = $scope.myFile;
        document.location.reload();
        console.log('file is ');
        console.dir(file);

        var uploadUrl = "/uploadCsv2";
        fileUpload.uploadFileToUrl(file, uploadUrl);
    };
	$scope.uploadcsv3 = function () {
        var file = $scope.myFile;
        document.location.reload();
        console.log('file is ');
        console.dir(file);

        var uploadUrl = "/uploadCsv3";
        fileUpload.uploadFileToUrl(file, uploadUrl);
    };
}]);

myApp.controller('AppCtrl', ['$scope', '$http', function ($scope, $http) {
    console.log("Hello World from controller");
    var refresh = function () {
        $http.get('/userDB').then(doneCallbacks, failCallbacks);
        $scope.user = null;
    };
    refresh();
    $scope.addUser = function () {
        console.log($scope.user);
        $http.post('/userDB', $scope.user).then(function (response) {
            console.log(response);
            refresh();
        });
    }
    $scope.remove = function (id) {
        console.log(id);
        $http.delete('/userDB/' + id).then(function (response) {
            refresh();
        });
    };
    $scope.edit = function (id) {
        console.log(id);
        $http.get('/userDB/' + id).then(function (response) {
            $scope.user = response.data;
        });
    };
    $scope.update = function () {
        console.log($scope.user._id);
        $http.put('/userDB/' + $scope.user._id, $scope.user).then(function (response) {
            refresh();
        });
    };
    $scope.deselect = function () {
        $scope.user = null;
    }
    $scope.upload = function (res) {
        res.redirect('/');
    }
    function doneCallbacks(res) {
        console.log("Data received");
        $scope.userDB = res.data;
    };
    function failCallbacks(err) {
        console.log(err.message);
    };
}]);