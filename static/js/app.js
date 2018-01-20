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
  .when("/dir/:dir*/", {
      templateUrl: "/html/dir.html",
      controller: "dirCtrl"
  })
  .when("/dir/", {
      templateUrl: "/html/dir.html",
      controller: "dirCtrl"
  })
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
    function split_dir_img(str)
    {
        var split = str.split('/')
        var ret = '/'
        for(var i = 1; i < split.length - 1; i++)
        {
            ret += split[i] + '/'
        }
        return ret
    }
    $scope.dir = split_dir_img($scope.img)
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
    $scope.dir = $routeParams.dir == undefined ? '/' : $routeParams.dir
    if ($scope.dir[0] != '/') $scope.dir = '/' + $scope.dir
    if ($scope.dir.length > 1 && $scope.dir[-1] != '/') $scope.dir += '/'

    // Just defaults for testing until API works
    $scope.children = ['test', 'test2']
    $scope.images = ['1', '2']

    $http.get("/api/dir" + $scope.img).then(
    function success(res) {
        if (res.object != "object") {
            console.warn('dir response is not json')
        }
        $scope.children = res.data['children'] === undefined ? [] : res.data['children']
        $scope.images = res.data['images'] == undefined ? [] : res.data['images']
    },
    function error(res) {
        console.warn('could not get directory', res.status, res.data)
    })

    $scope.reset = function () {
        $scope.label = $scope.old_label
    }
    console.log("dir");
});

app.controller("templateCtrl", function($scope, $routeParams, $http) {
    console.log("template");
    console.log($routeParams.template);
});
