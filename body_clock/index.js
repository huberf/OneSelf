//Getting all dependencies
var express = require('express');
var cookieParser = require('cookie-parser');
var session = require('express-session');
var app = express();
var nodemailer = require('nodemailer');
var bodyParser = require('body-parser');
var http = require('http').Server(app);
var io = require('socket.io')(http);

// Load events and any other local config
var events = {};

var getEvents = (id) => {
  return events;
}

var reloadEvents = () => {
  delete require.cache[require.resolve('./events.json')]
  events = require('./events.json');
}

reloadEvents();

//Setting up the port to listen to
app.set('port', (process.env.PORT || 5000));

//Setting up the resource directory
app.use(express.static(__dirname + '/public'));

app.use( bodyParser.urlencoded({ extended: false }));
app.use( bodyParser.json());

//Setting up cookie use
app.use(cookieParser());

//Setting up session handling
app.use(session({secret: 's3cr3tsSh0uldB3K3pt'}));

// views is directory for all template files
app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');


app.get('/', (req, res) => {
	res.render('pages/index', { events: getEvents('main') });
});

app.get('/example-clock', (req, res) => {
	res.render('pages/example');
});

app.get('/events/list', (req, res) => {
  res.send(getEvents('main'));
});

app.get('/events/reload', (req, res) => {
  reloadEvents();
  res.send({ status: 'success' });
});

io.sockets.on('connection', function(socket) {
  /*
  socket.on('test', function(data) {
    var data = [];
    io.emit('testsend', data);
  }
   */
});

http.listen(app.get('port'), function() {
  console.log('Node app is running on port ', app.get('port'));
});

