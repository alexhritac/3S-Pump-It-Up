const express = require('express'); // import express module
const app = express(); // create an express app
const port = 5000; // port on which the server will run
const ex = require('./config'); // import config file
const {sequelize} = require("./config"); // import sequelize instance from config file
const {QueryTypes} = require("sequelize"); // import sequelize query types
app.use(express.urlencoded({ extended: true })); // enable URL encoded bodies
app.use(express.json()); // enable JSON encoded bodies
var moment = require('moment-timezone'); // import moment-timezone module



app.listen(port, () => {
    console.log(`Server running on port ${port}`); // log message to console that server is running on the specified port
});


