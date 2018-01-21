var app = angular.module("Groundr", ["ngRoute"])
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
  .when("/template/:dir*/", {
      templateUrl: "/html/template.html",
      controller: "templateCtrl"
  })
  .when("/template", {
      templateUrl: "/html/template.html",
      controller: "templateCtrl"
   })
  .otherwise({
      templateUrl: "/html/404.html"
  });
});

app.controller("imgCtrl", function($scope, $routeParams, $http) {
    function Label() {
      this.class = "";
    }

    function Point(x, y) {
      this.x = x;
      this.y = y;
    }

    function Shape() {
      this.points = new Array();
      this.label = new Label();
    }

    var currentShape = 0;
    // var shapes = new Array();
    // shapes.push(new Shape());
    var paint;


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
    $scope.label = new Array();
    $scope.label.push(new Shape());

    $http.get("/api/label" + $scope.img).then(
    function success(res) {
        $scope.old_label = res.data
        $scope.label = $scope.old_label
        for (var i = 0; i < $scope.label.length; i++) {
          redraw(true, i);
        }
        // $scope.label.push(new Shape());
            newshape();
    },
    function error(res) {
        console.warn('could not get label', res.status, res.data)
    })

    $scope.x = ''
    $scope.template = {'classes': ['Buoy', 'STC', 'Dock'] } // Test default
    $http.get('/api/template' + $scope.dir).then(
    function success(res) {
        $scope.template = res.data
        if ($scope.template['classes'] == undefined) $scope.template['classes'] = []
        console.log($scope.template)
    },
    function error(res) {
        console.warn('could not get template', res.status, res.data)
    })

    $scope.save = function() {
        $http.post("/api/label" + $scope.img, $scope.label.slice(0,-1)).then(
        function success(res) {
            console.log("Saved");
        },
        function error(res) {
            console.warn("could not save label", res.status, res.data)
        })
    }

    $scope.reset = function () {
      $scope.old_label = {}
      $scope.label = new Array();
      $scope.label.push(new Shape());
      context.clearRect(0, 0, canvas.width, canvas.height);
    }

     $scope.undo = function () {
        $scope.label = $scope.old_label;
        $scope.label = $scope.label.slice(0,-1);
        clearanddraw();
        newshape();
    }

    var paint;
    var context;
    var done_drawing = false;

    $('#templates').change(function() {
      $scope.label[$scope.label.length-1].label.class = $('#templates').find(":selected").text();
    });

    function prepare() {
        canvas = document.getElementById('canvas')
        context = canvas.getContext("2d");

        canvas_back = document.getElementById('canvas_back')
        context_back = canvas_back.getContext("2d");

        $('#canvas_back').each(function() {
            var img1 = new Image();
            img1.onload = function() {
                context_back.drawImage(this, 0, 0);
            };
            img1.src = $scope.img_url;
            canvas_back.height = img1.height;
            canvas_back.width = img1.width;
            canvas.height = img1.height;
            canvas.width = img1.width;
        });

        $('#canvas').mousedown(function(e) {
            var mouseX = e.pageX - $('#canvas').parent().position().left - $('#canvas').position().left;
            var mouseY = e.pageY - $('#canvas').parent().position().top - $('#canvas').position().top;

            paint = true;
            addClick(mouseX, mouseY);
            redraw(false, $scope.label.length-1);
        });

        // TODO: Regular drawing
        $('#canvas').mousemove(function(e) {
            if (paint) {
            }
        });

        $('#canvas').mouseup(function(e) {
            paint = false;
        });

        $('#canvas').mouseleave(function(e) {
            paint = false;
        });
    }

    // var $div = $("<input>", {type: "text", "id": "txt_name"});

    function addClick(x, y, dragging) {
      var points = $scope.label[$scope.label.length-1].points;
        if (points.length > 0 && nearby(points[0], new Point(x,y), 20) == true) {
          done_drawing = true;
        }
        $scope.label[$scope.label.length-1].points.push(new Point(x,y));
    }


    function redraw(load, currentShape) {
      // console.log($scope.label)
      var points = $scope.label[currentShape].points;
      if (load == true)
      {
            points.push(points[0]);
      }

      // Check if we are closing the contour
        
        context.strokeStyle = "#df4b26";
        context.lineJoin = "round";
        context.lineWidth = 5;

        // TODO: Need to have layers so that we can refresh the drawings
        // Begin a path that we can fill when done
        context.beginPath();
        context.moveTo($scope.label[currentShape].points[0].x, $scope.label[currentShape].points[0].y);
        for (var i = 0; i < $scope.label[currentShape].points.length; i++) {

          // Draw a line from current point to previous
            if ($scope.label[currentShape].points.length > 1) {
                context.lineTo($scope.label[currentShape].points[i].x, $scope.label[currentShape].points[i].y);
            }

            // If we do not have a closed contour, keep drawing new circles
            if (!done_drawing)
            {
              context.arc(points[i].x, points[i].y, 5, 0, Math.PI * 2);
            }

            // Draw the lines
            context.stroke();

        }
        // Close the path
        context.closePath();

        // If we have a closed contour, color, add text, and create new shape
        if (done_drawing == true) {
            points.splice(-1,1)
            context.fillStyle = 'rgba(0,0,0,.2)';
            context.fill();
            context.fillStyle = "rgba(0,0,255,1)";
            context.font = "30px Arial"

            context.fillText(getdisplaylabel(currentShape), points[0].x, points[0].y-30); 

            $scope.old_label = $scope.label.slice()
            newshape();
            done_drawing = false;
        }

        if (load == true) {
            context.fillStyle = 'rgba(0,0,0,.2)';
            context.fill();
            context.fillStyle = "rgba(0,0,255,1)";
            context.font = "30px Arial"
            context.fillText(getdisplaylabel(currentShape), points[0].x, points[0].y-30); 
        }
    }

    function clearanddraw() {
      context.clearRect(0, 0, canvas.width, canvas.height);
      for (var i = 0; i < $scope.label.length; i++) {
          redraw(true, i);
      }
    }

    function getdisplaylabel(currentShape) {
        // display = "";
        // $.each($scope.label[currentShape].label, function(i,n){
        //   if (n != "") {
        //     display = n;
        //     return false;
        //   }
        // });
        return $scope.label[currentShape].label.class;
    }

    // Check if two points  are close to each other
    function nearby(p1, p2, amount) {
        if ((p1.x - p2.x) * (p1.x - p2.x) + (p1.y - p2.y) * (p1.y - p2.y) < amount * amount) {
            return true;
        } else {
            return false;
        }
    }

    // Add a new shape
    function newshape() {
      $scope.label.push(new Shape());
    }
    prepare();
});

app.controller("dirCtrl", function($scope, $routeParams, $http) {
    $scope.dir = $routeParams.dir == undefined ? '/' : $routeParams.dir
    if ($scope.dir[0] != '/') $scope.dir = '/' + $scope.dir
    if ($scope.dir.length > 1 && $scope.dir[-1] != '/') $scope.dir += '/'

    split = $scope.dir.split('/')
    if (split.length == 2) split = []
    else split = split.slice(1, -1)
    $scope.parents = []
    if (split.length > 0)
        $scope.parents.push({'name': split[0], 'href': split[0]})
    for (var i = 1; i < split.length; i++)
    {
        console.log($scope.parents)
        $scope.parents.push({'name': split[i], 'href': $scope.parents[i - 1]['href'] + '/' + split[i]})
    }

    // Just defaults for testing until API works
    $scope.children = []
    $scope.images = []

    $http.get("/api/dir" + $scope.dir).then(
    function success(res) {
        if (typeof(res.object) != "object") {
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

    $scope.upload = function() {
        var file_form = document.getElementById('grounder-upload-box')
        if (file_form.files.length != 1) {
            console.warn('No file selected')
            return
        }
        var formData = new FormData()
        formData.append('user-upload', file_form.files[0], file_form.files[0].name)
        $http.post("/api/upload" + $scope.dir, formData, {'headers': {'Content-Type': undefined}}).then(
        function success(res) {
          console.log('upload successful')
        },
        function error(res) {
          console.warn('error uploading file', res.status, res.data)
        })
    }

    $scope.newdir = ''
    $scope.createDirectory = function() {
      if ($scope.newdir.length < 1) {
        console.warn('cannot create directory with empty name')
        return
      }
      console.log('/api/dir' + $scope.dir +  $scope.newdir)
      $http.post('/api/dir' + $scope.dir + $scope.newdir).then(
      function success (res) {
        // should reload page or something here
        console.log('create directory successful')
      },
      function error (res) {
        console.warn('error creating directory', res.status, res.data)
      })
    }
    console.log("dir");
});

app.controller("templateCtrl", function($scope, $routeParams, $http) {
    $scope.dir = $routeParams.dir == undefined ? '/' : $routeParams.dir
    if ($scope.dir[0] != '/') $scope.dir = '/' + $scope.dir
    if ($scope.dir.length > 1 && $scope.dir[-1] != '/') $scope.dir += '/'

    split = $scope.dir.split('/')
    if (split.length == 2) split = []
    else split = split.slice(1, -1)
    $scope.parents = []
    if (split.length > 0)
        $scope.parents.push({'name': split[0], 'href': split[0]})
    for (var i = 1; i < split.length; i++)
    {
        console.log($scope.parents)
        $scope.parents.push({'name': split[i], 'href': $scope.parents[i - 1]['href'] + '/' + split[i]})
    }

    $scope.template = {'classes': ['Buoy', 'STC', 'Dock'] }

    $http.get('/api/template' + $scope.dir).then(
    function success(res) {
        $scope.template = res.data
        if ($scope.template['classes'] == undefined) $scope.template['classes'] = []

    },
    function error(res) {
        console.warn('could not get template', res.status, res.data)
    })

    $scope.remove = function(index) {
        $scope.template['classes'].splice(index, 1);
    }
    $scope.add = function() {
        $scope.template['classes'].push('');
    }
    $scope.save = function() {
        $http.post("/api/template" + $scope.dir, $scope.template).then(
        function success(res) {
            console.log('save good')
        },
        function error(res) {
            console.warn('could not save template', res.status, res.data)
        })
    }
});
