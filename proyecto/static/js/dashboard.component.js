angular.module('myApp',[]).config(function($httpProvider){
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
}).component('main',{
  templateUrl:'../template/dashboard.html'
})
.controller('controllerApp',['$http','$compile',
    function($http, $compile){
      var cm = this;
      //cm.username = "Javier Juan";
      cm.togleMenu = false;
      cm.mesage = function(){
        
      }
      cm.statusMenu = function(){
        if(cm.togleMenu)
          return cm.togleMenu = false;
        else
          return cm.togleMenu = true;  
      }
      cm.getUsers = function(urls){
        cm.datos=[];
        $http({
          method: 'GET',
          url: urls
          }).then(function(response){
                  // acciones a realizar cuando se recibe respuesta con éxito
                  //cm.datos = response.data;
                  //console.log(cm.datos)
                  var compiledeHTML = $compile(response)(this);
                  $("#d").append(compiledeHTML);
              }, function(error){
                  // acciones a realizar cuando se recibe una respuesta de error
                  cm.datos = [{'name': "Error!! ",'status': error.status}];
                  //console.log($scope.datos);
              });
      }
    }
  ]);