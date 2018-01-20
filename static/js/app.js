var app = angular.module("Grounder", ["ngRoute"])
app.config(function($routeProvider) {
  $routeProvider
  .when("/", {
      templateUrl: "/html/home.html"
  })
  .when("/img:img*", {
      templateUrl: "/html/img.html",
      controller: "imgCtrl"
  })
  .when("/img", { redirectTo: "/img/" })
  .when("/dir:dir*", {
      templateUrl: "/html/dir.html",
      controller: "dirCtrl"
  })
  .when("/dir", {redirectTo: "/dir/" })
  .when("/template:template*", {
      templateUrl: "/html/template.html",
      controller: "templateCtrl"
  })
  .when("/template", {redirectTo: "/template/"})
  .otherwise({
      templateUrl: "/html/404.html"
  });
});

app.controller("imgCtrl", function($scope, $routeParams, $http) {
    $scope.img = $routeParams.img;
    $scope.img_url = "/api/img" + $scope.img
    $scope.old_label = {}
    $scope.label = {}

    $http.get("/api/label" + $scope.img).then(
    function success(res) {
        $scope.old_label = res.data
        $scope.label = $scope.old_label
    },
    function error(res) {
        console.warn('could not get label', res.status, res.data)
    })

    $scope.save = function() {
        $http.post("/api/label" + $scope.img, $scope.label).then(
        function success(res) {
            console.log("Saved");
        },
        function error(res) {
            console.warn("could not save label", res.status, res.data)
        })
    }

    $scope.reset = function () {
        $scope.label = $scope.old_label
    }
});

app.controller("dirCtrl", function($scope, $routeParams, $http) {
    console.log("dir");
    console.log($routeParams.dir);
});

app.controller("templateCtrl", function($scope, $routeParams, $http) {
    console.log("template");
    console.log($routeParams.template);
});
