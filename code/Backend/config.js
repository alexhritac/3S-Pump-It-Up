const { Sequelize } = require('sequelize'); // import Sequelize module

/**
 * Create new Sequelize instance and connect to the 'mydb' database with the given credentials
 * @param {string} mydb - name of the database
 * @param {string} admin - username of the database
 * @param {string} Lololo123 - password of the database
 * @param {string} host - host of the database
 * @param {string} dialect - type of database (in this case, MySQL)
 */
const sequelize = new Sequelize('', '', '', {
    host: '',
    dialect: ''
});

try {
    sequelize.authenticate(); // try to authenticate the connection
    console.log('Connection has been established successfully.'); // if successful, log message
} catch (error) {
    console.error('Unable to connect to the database:', error); // if not successful, log error message
}
module.exports = {sequelize}; // export the sequelize instance to be used in other parts of the application