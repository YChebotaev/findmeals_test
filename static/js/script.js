angular.module('app', ['ui.bootstrap'])
    .controller('FindRecepieCtrl', ['$scope', '$http', '$rootScope', function ($scope, $http, $rootScope) {

        $scope.query = '';

        $scope.submit = function () {
            $http({
                method: 'GET',
                url: '/find_recepie',
                params: {
                    query: $scope.query
                }
            }).then(function(resp){
                $rootScope.recepies = resp.data.result
            }, function(resp) {
                document.write(resp.data)
            })
        };

    }]);