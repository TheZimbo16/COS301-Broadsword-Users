var express = require('express');
var app = express();
var mongojs = require('mongojs');
var fs = require('fs');
var db = mongojs('userDB', ['userDB']);
var bodyParser = require('body-parser');
var multer = require('multer');
var xlstojson = require("xls-to-json-lc");
var xlsxtojson = require("xlsx-to-json-lc");
var csv = require('fast-csv');
var csvjson = require('csvjson');
var path = require("path");
var worked = false;

app.use(express.static(__dirname + "/public"));
app.use(bodyParser.json());
app.get('/userDB', function (req, res) {
    console.log("I received a GET request");
    db.userDB.find(function (err, docs) {
        //console.log(docs);
        res.json(docs);
    });


});

app.post('/userDB', function (req, res) {
    console.log(req.body);
    db.userDB.insert(req.body, function (err, doc) {
        res.json(doc);
    });
});

app.delete('/userDB/:id', function (req, res) {
    var id = req.params.id;
    console.log(id);
    db.userDB.remove({_id: mongojs.ObjectId(id)}, function (err, doc) {
        res.json(doc);
    })
});

app.get('/userDB/:id', function (req, res) {
    var id = req.params.id;
    console.log(id);
    db.userDB.findOne({_id: mongojs.ObjectId(id)}, function (err, doc) {
        res.json(doc);
    })
});

app.put('/userDB/:id', function (req, res) {
    var id = req.params.id;
    console.log(req.body.name);
    db.userDB.findAndModify({
        query: {_id: mongojs.ObjectId(id)},
        update: {
            $set: {
                name: req.body.name,
                surname: req.body.surname,
                number: req.body.studentnumber,
                isAuthenticated: req.body.isauthenticated,
                isAdmin: req.body.isadmin
            }
        },
        new: true
    }, function (err, doc) {
        res.json(doc);
    });
});

var storage = multer.diskStorage({ //multers disk storage settings
    destination: function (req, file, cb) {
        cb(null, './uploads/')
    },
    filename: function (req, file, cb) {
        var datetimestamp = Date.now();
        cb(null, file.fieldname + '-' + datetimestamp + '.' + file.originalname.split('.')[file.originalname.split('.').length - 1])
    }
});

var upload = multer({ //multer settings
    storage: storage,
    fileFilter: function (req, file, callback) { //file filter
        if (['xls', 'xlsx', 'csv',].indexOf(file.originalname.split('.')[file.originalname.split('.').length - 1]) === -1) {
            return callback(new Error('Wrong extension type'));
        }
        callback(null, true);
    }
}).single('file');

/** API path that will upload the files */
app.post('/upload1', function (req, res) {
    var exceltojson;
    upload(req, res, function (err) {
        if (err) {
            res.json({error_code: 1, err_desc: err});
            return;
        }
        /** Multer gives us file info in req.file object */
        if (!req.file) {
            res.json({error_code: 1, err_desc: "No file passed"});
            return;
        }
        /** Check the extension of the incoming file and
         *  use the appropriate module
         */
        if (req.file.originalname.split('.')[req.file.originalname.split('.').length - 1] === 'xlsx') {
            exceltojson = xlsxtojson;
        } else {
            exceltojson = xlstojson;
        }
        try {
            exceltojson({
                input: req.file.path,
                output: null, //since we don't need output.json
                lowerCaseHeaders: false,
                headerSent: true,
            }, function (err, result) {
                if (err) {
                    return res.json({error_code: 1, err_desc: err, data: null});
                }
                var id = req.params.id;
                //console.log(id);
                db.userDB.insert(result, function (err, doc) {

                    res.json({error_code: 0, err_desc: null, data: result});

                    worked = true;
                });
            });

        } catch (e) {
            res.json({error_code: 1, err_desc: "Corrupted excel file"});
        }
    })
});

app.post('/upload', function (req, res) {
    var exceltojson;
    upload(req, res, function (err) {
        if (err) {
            res.json({error_code: 1, err_desc: err});
            return;
        }
        /** Multer gives us file info in req.file object */
        if (!req.file) {
            res.json({error_code: 1, err_desc: "No file passed"});
            return;
        }
        /** Check the extension of the incoming file and
         *  use the appropriate module
         */
        if (req.file.originalname.split('.')[req.file.originalname.split('.').length - 1] === 'xlsx') {
            exceltojson = xlsxtojson;
        } else {
            exceltojson = xlstojson;
        }
        try {
            exceltojson({
                input: req.file.path,
                output: null, //since we don't need output.json
                lowerCaseHeaders: false,
                headerSent: true,
            }, function (err, result) {
                if (err) {
                    return res.json({error_code: 1, err_desc: err, data: null});
                }
                var id = req.params.id;
                db.userDB.find(function (err, res) {
                    for (var i = 0; i < result.length; i++) {
                        console.log(res[i]._id);
                        console.log(result[i].isAdmin);
                        db.userDB.findAndModify({
                            query: {_id: mongojs.ObjectId(res[i]._id)},
                            update: {
                                $set: {
                                    name: result[i].name,
                                    surname: result[i].surname,
                                    number: result[i].studentnumber,
                                    isAuthenticated: result[i].isauthenticated,
                                    isAdmin: result[i].isadmin
                                }
                            },
                            new: true
                        }, function (err, doc) {

                        });
                    };
                    worked = true;
                });
            });
        } catch (e) {
            res.json({error_code: 1, err_desc: "Corrupted excel file"});
        }
    })
});

app.post('/upload2', function (req, res) {
    var exceltojson;
    upload(req, res, function (err) {
        if (err) {
            res.json({error_code: 1, err_desc: err});
            return;
        }
        /** Multer gives us file info in req.file object */
        if (!req.file) {
            res.json({error_code: 1, err_desc: "No file passed"});
            return;
        }
        /** Check the extension of the incoming file and
         *  use the appropriate module
         */
        if (req.file.originalname.split('.')[req.file.originalname.split('.').length - 1] === 'xlsx') {
            exceltojson = xlsxtojson;
        } else {
            exceltojson = xlstojson;
        }
        try {

            exceltojson({
                input: req.file.path,
                output: null, //since we don't need output.json
                lowerCaseHeaders: false,
                headerSent: true,
            }, function (err, result) {
                if (err) {
                    return res.json({error_code: 1, err_desc: err, data: null});
                }
                var id = req.params.id;
                //console.log(id);
                db.userDB.find(function (err, result) {
                    console.log(result.number);

                    for (var i = 0; i < result.length; i++) {

                        //console.log(result[i]._id);
                        db.userDB.remove({_id: mongojs.ObjectId(result[i]._id)}, function (err, doc) {

                        })
                    }
                    worked = true;
                });

            });

        } catch (e) {
            res.json({error_code: 1, err_desc: "Corrupted excel file"});
        }
    })
});

app.post('/uploadCsv1', function (req, res){
    var csv1;
    upload(req, res, function (err) {
        if (err) {
            res.json({error_code: 1, err_desc: err});
            return;
        }
        /** Multer gives us file info in req.file object */
        if (!req.file) {
            res.json({error_code: 1, err_desc: "No file passed"});
            return;
        }
        /** Check the extension of the incoming file and
         *  use the appropriate module
         */
        if (req.file.originalname.split('.')[req.file.originalname.split('.').length - 1] === 'csv') {
            csv1 = csv;
        }

        try {
          
			
           
                  
					
					
					var data1 = fs.readFileSync(path.join('./uploads/', req.file.filename), { encoding : 'utf8'});
						/*
						{
							delimiter : <String> optional default is ","
							quote     : <String|Boolean> default is null
						}
						*/
						var options = {
						  delimiter : ',', // optional 
						  quote     : '"' // optional 
						};
						var json =csvjson.toSchemaObject(data1, options);
						    db.userDB.insert(json, function (err, doc) {

							res.json({error_code: 0, err_desc: null, data: json});

							worked = true;
						});
               
              

        
        }
        catch(e){
            res.json({error_code: 1, err_desc: "Corrupted file"});
        }
    });

});

app.post('/uploadCsv2', function (req, res){
    var csv1;
    upload(req, res, function (err) {
        if (err) {
            res.json({error_code: 1, err_desc: err});
            return;
        }
        /** Multer gives us file info in req.file object */
        if (!req.file) {
            res.json({error_code: 1, err_desc: "No file passed"});
            return;
        }
        /** Check the extension of the incoming file and
         *  use the appropriate module
         */
        if (req.file.originalname.split('.')[req.file.originalname.split('.').length - 1] === 'csv') {
            csv1 = csv;
        }

        try {
          
			
           
                  
					
					
					var data1 = fs.readFileSync(path.join('./uploads/', req.file.filename), { encoding : 'utf8'});
						/*
						{
							delimiter : <String> optional default is ","
							quote     : <String|Boolean> default is null
						}
						*/
						var options = {
						  delimiter : ',', // optional 
						  quote     : '"' // optional 
						};
						var json =csvjson.toSchemaObject(data1, options);
						    db.userDB.find(function (err, res) {
								

								for (var i = 0; i < json.length; i++) {

									//console.log(result[i]._id);
									db.userDB.remove({_id: mongojs.ObjectId(res[i]._id)}, function (err, doc) {

									})
								}
								worked = true;
							});
               
              

        
        }
        catch(e){
            res.json({error_code: 1, err_desc: "Corrupted file"});
        }
    });

});

app.post('/uploadCsv3', function (req, res){
    var csv1;
    upload(req, res, function (err) {
        if (err) {
            res.json({error_code: 1, err_desc: err});
            return;
        }
        /** Multer gives us file info in req.file object */
        if (!req.file) {
            res.json({error_code: 1, err_desc: "No file passed"});
            return;
        }
        /** Check the extension of the incoming file and
         *  use the appropriate module
         */
        if (req.file.originalname.split('.')[req.file.originalname.split('.').length - 1] === 'csv') {
            csv1 = csv;
        }

        try {
          
			
           
                  
					
					
					var data1 = fs.readFileSync(path.join('./uploads/', req.file.filename), { encoding : 'utf8'});
						/*
						{
							delimiter : <String> optional default is ","
							quote     : <String|Boolean> default is null
						}
						*/
						var options = {
						  delimiter : ',', // optional 
						  quote     : '"' // optional 
						};
						var json =csvjson.toSchemaObject(data1, options);
						 db.userDB.find(function (err, res) {
								for (var i = 0; i < json.length; i++) {
									console.log(res[i]._id);
									console.log(json[i].isadmin);
									db.userDB.findAndModify({
										query: {_id: mongojs.ObjectId(res[i]._id)},
										update: {
											$set: {
												name: json[i].name,
												surname: json[i].surname,
												number: json[i].studentnumber,
												isauthenticated: json[i].isauthenticated,
												isadmin: json[i].isadmin
											}
										},
										new: true
									}, function (err, doc) {

									});
								};
								worked = true;
							});
               
              

        
        }
        catch(e){
            res.json({error_code: 1, err_desc: "Corrupted file"});
        }
    });

});

app.get('/', function (req, res) {
    res.sendFile(__dirname + "/index.html");
});

app.listen(process.argv[2]);
console.log("Server running on port" + process.argv[2]);