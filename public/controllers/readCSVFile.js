MyApp.query(); 
    angular.
      module('myApp').
        controller: ['MyApp',
         function MyAppController(MyApp) {
            this.myApp = MyApp.query();
          }
        ]
      });