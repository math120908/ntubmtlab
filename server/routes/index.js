var express = require('express');
var router = express.Router();
require('datejs');
var Q = require('q');

//RegExp
router.param(function(name, fn){
   if (fn instanceof RegExp) {
      return function(req, res, next, val){
         var captures;
         if (captures = fn.exec(String(val))) {
            req.params[name] = captures[0];
            next();
         } else {
            next('route');
         }
      }
   }
});


var placeMapping = {"1":"New 1","2":"New 3","3":"Old"};
router.param('year', /^\d+$/);
router.param('month', /^\d+$/);
router.param('day', /^\d+$/);
router.param('sttime', /^\d+$/);
router.param('place', /^\d+$/);

function is_mobile(req) {
   console.log(req.header('user-agent'));
   if (/mobile/i.test(req.header('user-agent'))) return true;
   else return false;
};

/* GET home page. */
homepage = function(req, res) {
    var db = req.db;
    var collection = db.get('data');
    var lastupdate = "NULL";

    var searchMonth = [Date.today().toString('yyyy/MM'),Date.today().add(1).month().toString('yyyy/MM')]; 
    var wakeupInfos = [];

    var dbfindOne = function( query ){
       var deferred = Q.defer();
       collection.findOne(query, function (err, data) {
          if (err) deferred.reject(err); // rejects the promise with `er` as the reason
          else deferred.resolve(data); // fulfills the promise with `data` as the value
       });
       return deferred.promise; // the promise is returned
    }

    dbfindOne({"date": searchMonth[0], "place": "wakeup"}).then(function(ents){
       if(ents) wakeupInfos.push( ents );
       return dbfindOne({"date": searchMonth[1], "place": "wakeup"});
    }).then(function(ents){
       if(ents) wakeupInfos.push( ents );
       return dbfindOne({"update": 0});
    }).then(function(ents){
       lastupdate = ents['savetime'];
       res.render('index', 
          { title: 'NTU Badminton Information System', 
             lastupdate: lastupdate,
          wakeupInfos: wakeupInfos,
          isMobile: is_mobile(req)
          });
    });
}
router.get('/', homepage);

function dbents2dict( dbents ){
   var dbdict = {};
   dbents.forEach(function(ele){
      delete ele['_id'];
      var time = ele.time;
      var place = ele.place;
      if( typeof(dbdict[time]) == 'undefined' ){
         dbdict[time] = {};
      }
      dbdict[time][place] = ele;
   }); 
   return dbdict;
}

router.get('/q/:year/:month/:day',function(req,res){
    var collection = req.db.get('data');
    queryEntry = { "date": req.params.year + "/" + req.params.month + "/" + req.params.day }

    collection.find( queryEntry, function(err,ents){
       var dbdict = dbents2dict(ents)
       //console.log(dbdict);
       res.json(dbdict);
    });
});

//router.get('/q/:year/:month/:day/:sttime/:place',function(req,res){
//    var collection = req.db.get('data');
//    queryEntry = { "date": req.params.year + "/" + req.params.month + "/" + req.params.day,
//   "time": parseInt(req.params.sttime),
//   "place": placeMapping[req.params.place]
//    }
//
//    collection.findOne( queryEntry, function(err,ents){
//       res.json(ents);
//    });
//});

router.use('/q',function(req,res,next){
    var err = new Error('Error Query Format');
    err.status = 404;
    next(err);
});

router.use('/', function(req, res){
   res.redirect('/');
});

module.exports = router;
