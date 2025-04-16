const express = require('express');
const path = require('path');
const favicon = require('serve-favicon');
const logger = require('morgan');
const cors = require('cors');

require('dotenv').config();

const { connection } = require('./config/database.js');

// Execution of the express app
const app = express();

app.use('/plots', express.static(path.join(__dirname, 'public/plots')));


// Connect to the BNX database
connection();

// Cross-Origin Resource Sharing (CORS) middleware
app.use(cors({
  origin: 'http://localhost:3000',  // Adjust the frontend's port if different
  methods: ['GET', 'POST'],
  credentials: true
}));

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Configure both serve-favicon & static middleware
// to serve from the production 'build' folder
// app.use(favicon(path.join(__dirname, 'build', 'favicon.ico')));
// app.use(express.static(path.join(__dirname, 'build')));

// Serve favicon from the client build directory
app.use(favicon(path.join(__dirname, '../bnx_client/build/favicon.ico')));

// Serve static files from the client build directory
app.use(express.static(path.join(__dirname, '../bnx_client/build')));

app.use('/plots', express.static(path.join(__dirname, '../bnx_client/public/plots')));



app.use((req, res, next) => {
  res.setTimeout(300000, () => { // 5 minutes
    res.status(503).send("Server timed out");
  });
  next();
});


// Put API routes here, before the "catch all" route

// Yahoo Finance Web Scraper API
app.use(
  '/api/yahoo-finance', 
  require('./routes/api/yahoo-finance.js')
);

// User API
app.use(
  '/api/users', 
  require('./routes/api/users.js')
);

// Saved Data API
app.use(
  '/api/saved-data', 
  require('./routes/api/saved-data.js')
);

// The following "catch all" route (note the *) is necessary
// to return the index.html on all non-AJAX requests
app.get('/*', function(req, res) {
    res.sendFile(path.join(__dirname, '../bnx_client/build/index.html'));
  });

// Configure to use port 3001 instead of 3000 during
// development to avoid collision with React's dev server
const port = process.env.PORT || 3001;

app.listen(port, function() {
  console.log(`Express app running on port ${port}`)
});