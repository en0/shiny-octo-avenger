var app = angular.module('myApp', ['ngRoute','ui.bootstrap']);

app.config(['$routeProvider', function($routeProvider) {
    $routeProvider

        /** Private Routes **/
        .when("/", {templateUrl: "partials/feed.php", controller: "homeCtrl"})
        .when("/feed", {templateUrl: "partials/feed.php", controller: "homeCtrl"})
        .when("/about", {templateUrl: "partials/about.php", controller: "aboutCtrl"})
        .when("/logout", {templateUrl: "partials/logout.php", controller: "logoutCtrl"})

        /** Restricted Routes **/
        .when("/users", {templateUrl: "partials/users.php", controller: "usersCtrl", role:'admin'})

        /** Public Routes **/
        .when("/login", {templateUrl: "partials/login.php", controller: "loginCtrl", isPublic: true})
        .when("/login/:rurl", {templateUrl: "partials/login.php", controller: "loginCtrl", isPublic: true})
        .when("/register", {templateUrl: "partials/register.php", controller: "registerCtrl", isPublic: true})
        .when("/register/complete", {templateUrl: "partials/register_complete.php", controller: "registerCtrl", isPublic: true})
        .when("/404", {templateUrl: "partials/404.php", controller: "nullCtrl", isPublic: true})
        .when("/testing", { templateUrl: "partials/testing.php", controller: "testingCtrl", isPublic: true})
        .otherwise({ redirectTo: '/404' });
}]);

