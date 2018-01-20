var app = angular.module("Grounder", ["ngRoute"])
app.config(function($routeProvider) {
  $routeProvider
  .when("/", {
      templateUrl: "/html/home.html"
  })
  .when("/img/:img*", {
      templateUrl: "/html/img.html",
      controller: "imgCtrl"
  })
  .when("/dir/:dir*", {
      templateUrl: "/html/dir.html",
      controller: "dirCtrl"
  })
  .when("/template/:template*", {
      templateUrl: "/html/template.html",
      controller: "templateCtrl"
  })
  .otherwise({
      templateUrl: "/html/404.html"
  });
});

app.controller("imgCtrl", function($scope, $routeParams) {
    console.log("img");
    console.log($routeParams.img);
});

app.controller("dirCtrl", function($scope, $routeParams) {
    console.log("dir");
    console.log($routeParams.dir);
});

app.controller("templateCtrl", function($scope, $routeParams) {
    console.log("template");
    console.log($routeParams.template);
});
