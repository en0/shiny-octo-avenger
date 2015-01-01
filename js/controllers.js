'use strict'
app.controller('rootCtrl', ['$rootScope', '$auth', '$location', '$route', function($rootScope, $auth, $loc, $route) {

    $rootScope.authority = $auth;

    $rootScope.changeView = function(view) {
        $loc.url(view);
    };

    $rootScope.$on("$routeChangeStart", function(event, next, current) {
        var isPublic = next.isPublic || false;
        var reqRole = next.role || false;
        var returnUrl = btoa($loc.$$path);
        console.log(next.role != false);
        $auth.syncAuthority().then(function(result) {
            if(!$auth.isAuthenticated && !isPublic) {
                $rootScope.changeView('/login/'+returnUrl);
            } else if (reqRole != false && !$auth.isInRole(reqRole)) {
                $rootScope.changeView('/404');
            }
        }, function(error) {
            console.log(error);
            if(!isPublic) {
                $rootScope.changeView('/login/'+returnUrl);
            }
        });
    });

    $rootScope.setMenu = function(menu) {
        if($rootScope.authority.isAuthenticated) {
            $rootScope.menu = [
                {
                    'label' : 'Navigation',
                    'type' : 'list',
                    'items' : [
                        { 'label' : 'Feed', 'type' : 'url', 'target' : '#/feed', 'enabled' : true },
                        { 'label' : 'Pictures', 'type' : 'url', 'target' : '#/pictures', 'enabled' : true },
                        { 'label' : 'Music', 'type' : 'url', 'target' : '#/music', 'enabled' : true },
                        { 'label' : 'Videos', 'type' : 'url', 'target' : '#/video', 'enabled' : true },
                        { 'label' : 'File Manager', 'type' : 'url', 'target' : '#/files', 'enabled' : true },
                        { 'label' : 'Manage Users', 'type' : 'url', 'target' : '#/users', 'enabled' : $auth.isInRole('admin') },
                        { 'type' : 'divider', 'enabled' : true },
                        { 'label' : 'About', 'type' : 'url', 'target' : '#/about', 'enabled' : true },
                        { 'label' : 'Prefrences', 'type' : 'url', 'target' : '#/preferences', 'enabled' : true },
                        { 'label' : 'Logout', 'type' : 'url', 'target' : '#/logout', 'enabled' : true },
                    ]
                }
            ];
        } else {
            $rootScope.menu = [
                { 'label' : 'Request Membership', 'type' : 'url', 'target' : '#/register', 'enabled' : true },
            ];
        }
    
        if(typeof(menu) !== 'undefined' && menu != null) {
            $rootScope.menu.push({ 'type' : 'divider', });
            angular.forEach(menu, function(item) {
                $rootScope.menu.push(item);
            });
        }
    };

}]);

app.controller('homeCtrl', ['$scope', function($scope) {
    $scope.setMenu([
            { 
                'label' : 'Testing', 
                'type' : 'fn', 
                'target' : function() { alert('Hello, World'); }
            },
    ]);
}]);

app.controller('aboutCtrl', ['$scope', function($scope) {
    $scope.setMenu(null);
}]);

app.controller('logoutCtrl', ['$scope', function($scope) {
    $scope.authority.logout();
    $scope.changeView('/');
}]);

app.controller('loginCtrl', ['$scope', '$routeParams',function($scope,$routeParams) {
    $scope.setMenu(null);
    $scope.user = {};

    // Plan to send back to wherever they came from if we can.
    try { $scope.rurl = atob($routeParams['rurl']); } catch(err){ $scope.rurl = '/'; }

    $scope.submit = function(user) {
        $scope.alerts = [];
        if($scope.signFormIn.$error.required === false) {
            $scope.authority.login(user.username, user.password)
            .then( function (data) {
                if(!$scope.authority.isAuthenticated) 
                    $scope.alerts.push({msg: "Incorrect username or password", type: 'danger'});
                else {
                    $scope.alerts.push({msg: "Login Successfull!", type: 'success'});
                    $scope.changeView($scope.rurl);
                }
            }, function(error) {
                $scope.alerts.push({msg: "Incorrect username or password", type: 'danger'});
            });
        } 
    };

    $scope.closeAlert = function(index) {
        $scope.alerts.splice(index, 1);
    };

}]);

app.controller("registerCtrl", ['$scope', '$registration', function($scope, $registration) {

    $scope.setMenu([{ 'label' : 'Login', 'type' : 'url', 'target' : '#/login', 'enabled' : true }]);
    
    $scope.user = {};
    $scope.alerts = [{
        msg: "Registration is only open to friends and family.  If you don't know if you are my friend or family then don't bother to register.",
        type: "success",
    }];

    $scope.submit = function(user) {
        $scope.alerts = [];
        $registration.put(user)
        .then(function(result) {
            $scope.changeView('register/complete');
        }, function(error) {
            console.log(error);
            $scope.user = {};
            $scope.alerts.push({msg: 'Registration failed: ' + error.msg, type: 'danger'});
        });
    };

    $scope.closeAlert = function(index) {
        $scope.alerts.splice(index, 1);
    };
}]);

app.controller("usersCtrl", ['$scope', '$registration', '$users', '$roles', '$modal', function($scope, $registration, $users, $roles, $modal) {

    $scope.alerts = [];

    $scope.loadUsers = function() {
        $registration.getList().then(function(result) { $scope.pending = result; });
        $users.getList().then(function(result) { $scope.users = result; });
        $roles.getList().then(function(result) { $scope.roles = result; });
    }

    $scope.removeUser = function(id) {
        $users.remove(id).then(function(result) {
            $scope.loadUsers();
        }, function(error) {
            $scope.alerts.push({
                msg: "Failed to remove user.",
                type: "danger"
            });
        });
    }

    $scope.removePending = function(id) {
        $registration.remove(id).then(function(result) {
            $scope.loadUsers();
        }, function(error) {
            $scope.alerts.push({
                msg: "Failed to remove membership request.",
                type: "danger"
            });
        });
    }

    $scope.removeRole = function(id) {
        $roles.remove(id).then(function(result) {
            $scope.loadUsers();
        }, function(error) {
            $scope.alerts.push({
                msg: "Failed to remove role.",
                type: "danger"
            });
        });
    }

    $scope.showUserDetails = function (id) {
        $users.getDetail(id).then(function (result) {
            $modal.open({
                templateUrl: '/partials/user_details.php',
                controller: 'modalCtrl',
                resolve: { 
                    item: function() { 
                        return { 
                            user: result,
                            roles: $scope.roles,
                        };
                    } 
                }
            }).result.then(function(result) {
                $users.save(result.user).then(function (result) {
                    $scope.loadUsers();
                }, function (error) {
                    $scope.alerts.push({
                        msg: "Failed to save changes.",
                        type: "danger"
                    });
                });
            });
        });
    };

    $scope.showPendingDetails = function (id) {
        $registration.getDetail(id).then(function (result) {
            var modalInstance = $modal.open({
                templateUrl: '/partials/pending_details.php',
                controller: 'modalCtrl',
                resolve: { 
                    item: function() { 
                        return { 
                            user: result,
                            roles: $scope.roles,
                        };
                    } 
                }
            }).result.then(function(result) {
                $registration.save(result.user).then(function (result) {
                    $scope.loadUsers();
                }, function (error) {
                    $scope.alerts.push({
                        msg: "Failed to save changes.",
                        type: "danger"
                    });
                });
            });
        });
    };

    $scope.showNewUser = function() {
        var modalInstance = $modal.open({
            templateUrl: '/partials/user_new.php',
            controller: 'modalCtrl',
            resolve: {
                item: function() { 
                    return {
                        user: { storageLimit: 1024, active: true , roles: ['user']},
                        roles: $scope.roles,
                    };
                },
             }
        }).result.then(function(result) {
            $users.put(result.user).then(function (result) {
                $scope.loadUsers();
            }, function (error) {
                $scope.alerts.push({
                    msg: "Failed to save changes.",
                    type: "danger"
                });
            });
        });
    };

    $scope.showRoleDetails = function (id) {
        $roles.getDetail(id).then(function (result) {
            var modalInstance = $modal.open({
                templateUrl: '/partials/role_details.php',
                controller: 'modalCtrl',
                resolve: { item: function() { return result; } }
            }).result.then(function(result) {
                $roles.save(result).then(function (result) {
                    $scope.loadUsers();
                }, function (error) {
                    $scope.alerts.push({
                        msg: "Failed to save changes.",
                        type: "danger"
                    });
                });
            });
        });
    };

    $scope.showNewRole = function() {
        var modalInstance = $modal.open({
            templateUrl: '/partials/role_new.php',
            controller: 'modalCtrl',
            resolve: { item: function() { return {}; }, }
        }).result.then(function(result) {
            $roles.put(result).then(function (result) {
                $scope.loadUsers();
            }, function (error) {
                $scope.alerts.push({
                    msg: "Failed to save changes.",
                    type: "danger"
                });
            });
        });
    };

    $scope.setMenu([
            { 
                label: 'Create User', 
                type: 'fn', 
                target: $scope.showNewUser,
            },
            {
                label: 'Create Role',
                type: 'fn',
                target: $scope.showNewRole,
            },
    ]);

    $scope.closeAlert = function(index) { $scope.alerts.splice(index, 1); };
    $scope.loadUsers();
}]);

app.controller("modalCtrl", ['$scope', '$modalInstance', 'item', function($scope, $modalInstance, item) {
    $scope.item = item;
    console.log(item);
    $scope.ok = function () {console.log($scope.item); $modalInstance.close($scope.item); };
    $scope.cancel = function () { $modalInstance.dismiss('cancel'); };
}]);

app.controller("nullCtrl", ['$scope', function($scope) {
    $scope.setMenu(null);
}]);

app.controller("testingCtrl", ['$scope', function($scope) {
    $scope.setMenu(null);
    console.log('testing');
}]);
