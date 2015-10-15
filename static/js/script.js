angular.module('app', ['ui.bootstrap', 'ngTagsInput'])
    .controller('FindRecepieCtrl', ['$scope', '$http', '$rootScope', function ($scope, $http, $rootScope) {

        $scope.query = '';
        $scope.ingredientsInclude = [];
        $scope.ingredientsExclude = [];

        $scope.ingredientsAutocomplete = function ($query) {
            return $http({
                method: 'GET',
                url: '/ingredients_autocomplete',
                params: {
                    query: $query
                }
            })
        };

        $scope.submit = function () {
            $http({
                method: 'GET',
                url: '/find_recepie',
                params: {
                    search: $scope.query,
                    include: JSON.stringify($scope.ingredientsInclude),
                    exclude: JSON.stringify($scope.ingredientsExclude)
                }
            }).then(function(resp){
                $rootScope.recepies = resp.data.result
            }, function(resp) {
                document.write(resp.data)
            })
        };

    }]);