const createError = require('http-errors');
const express = require('express');
const path = require('path');
const cookieParser = require('cookie-parser');
const logger = require('morgan');
const connectDb = require('./db'); // Import the connect function

// Import the todo router
var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');
const registerRouter = require('./routes/authentication/register');
// const registerRouter = require('./routes/authentication/'); // Import the register router

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/users', usersRouter);
app.use('/auth', registerRouter);
// app.use('/auth', registerRouter);  // Adds the registration route under '/auth/register'
// app.use('/auth', protectedRouter); // Adds the protected route under '/auth/protected'

// Connect to the database
connectDb()
  .then(db => {
    // Test the connection to the database
    return db.one('SELECT $1 AS value', 123);
  })
  .then(data => {
    console.log('DATA:', data.value);
  })
  .catch(error => {
    console.log('ERROR:', error);
  });

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
