const express = require('express'); // import express js module
const cors = require('cors');
const app = express(); // create express js app
app.use(cors());
const port = 5000; // set express js port
const ex = require("./config"); // import config file
const{sequelize} = require("./config") // import sequelize instance from config file
const{QuesryTypes} = require("sequelize");
app.use(express.urlencoded({extended:true}));  // enable URL encoded bodies
app.use(express.json()); // enable JSON encoded bodies
var strftime = require('strftime');

let realTimeQuery, historicalQuery;
var sensorDataHistorical = {};
var sensorDataRealTime = {};


(async function()  {
while(true) {

const {QueryTypes} = require('sequelize');

var now = new Date();
now.setDate(now.getDate()-31);
var historical = strftime('%Y-%m-%d %H:%M:%S',now)

console.log(historical);

historicalQuery = await sequelize.query(
    "SELECT date, abs210, abs254, sac254, uvt254, abs360, turbidity, acidity, conductivity, trp, bod, cod, no2, no3 FROM sensors WHERE date >= ?;",
    { replacements:[historical], type: sequelize.QueryTypes.SELECT }
);
    sensorDataHistorical = {};
    historicalQuery.forEach(row => {
        sensorDataHistorical['abs210'] = sensorDataHistorical['abs210'] || [];
        sensorDataHistorical['abs210'].push({ date: row.date, value: row.abs210 });

        sensorDataHistorical['abs254'] = sensorDataHistorical['abs254'] || [];
        sensorDataHistorical['abs254'].push({ date: row.date, value: row.abs254 });

        sensorDataHistorical['sac254'] = sensorDataHistorical['sac254'] || [];
        sensorDataHistorical['sac254'].push({ date: row.date, value: row.sac254 });

        sensorDataHistorical['uvt254'] = sensorDataHistorical['uvt254'] || [];
        sensorDataHistorical['uvt254'].push({ date: row.date, value: row.uvt254 });

        sensorDataHistorical['abs360'] = sensorDataHistorical['abs360'] || [];
        sensorDataHistorical['abs360'].push({ date: row.date, value: row.abs360 });

        sensorDataHistorical['turbidity'] = sensorDataHistorical['turbidity'] || [];
        sensorDataHistorical['turbidity'].push({ date: row.date, value: row.turbidity });

        sensorDataHistorical['acidity'] = sensorDataHistorical['acidity'] || [];
        sensorDataHistorical['acidity'].push({ date: row.date, value: row.acidity });

        sensorDataHistorical['conductivity'] = sensorDataHistorical['conductivity'] || [];
        sensorDataHistorical['conductivity'].push({ date: row.date, value: row.conductivity });

        sensorDataHistorical['trp'] = sensorDataHistorical['trp'] || [];
        sensorDataHistorical['trp'].push({ date: row.date, value: row.trp });

        sensorDataHistorical['bod'] = sensorDataHistorical['bod'] || [];
        sensorDataHistorical['bod'].push({ date: row.date, value: row.bod });

        sensorDataHistorical['cod'] = sensorDataHistorical['cod'] || [];
        sensorDataHistorical['cod'].push({ date: row.date, value: row.cod });

        sensorDataHistorical['no2'] = sensorDataHistorical['no2'] || [];
        sensorDataHistorical['no2'].push({ date: row.date, value: row.no2 });

        sensorDataHistorical['no3'] = sensorDataHistorical['no3'] || [];
        sensorDataHistorical['no3'].push({ date: row.date, value: row.no3 });
    });

    //console.log(sensorDataHistorical);
await new Promise(res => setTimeout(res, 60 * 60 * 1000)); // 60 minutes delay
}})();


(async function()  {
while(true) {

    const {QueryTypes} = require('sequelize');

    var now = new Date();
    //now.setHours(now.getHours()-1);
    now.setDate(now.getDate()-7);
    var realTime = strftime('%Y-%m-%d %H:%M:%S',now)

    console.log(realTime);

    realTimeQuery = await sequelize.query(
        "SELECT date, abs210, abs254, sac254, uvt254, abs360, turbidity, acidity, conductivity, trp, bod, cod, no2, no3 FROM sensors WHERE date >= ?;",
        { replacements:[realTime], type: sequelize.QueryTypes.SELECT }
    )
        sensorDataRealTime = {};
        realTimeQuery.forEach(row => {
            sensorDataRealTime['abs210'] = sensorDataRealTime['abs210'] || [];
            sensorDataRealTime['abs210'].push({ date: row.date, value: row.abs210 });

            sensorDataRealTime['abs254'] = sensorDataRealTime['abs254'] || [];
            sensorDataRealTime['abs254'].push({ date: row.date, value: row.abs254 });

            sensorDataRealTime['sac254'] = sensorDataRealTime['sac254'] || [];
            sensorDataRealTime['sac254'].push({ date: row.date, value: row.sac254 });

            sensorDataRealTime['uvt254'] = sensorDataRealTime['uvt254'] || [];
            sensorDataRealTime['uvt254'].push({ date: row.date, value: row.uvt254 });

            sensorDataRealTime['abs360'] = sensorDataRealTime['abs360'] || [];
            sensorDataRealTime['abs360'].push({ date: row.date, value: row.abs360 });

            sensorDataRealTime['turbidity'] = sensorDataRealTime['turbidity'] || [];
            sensorDataRealTime['turbidity'].push({ date: row.date, value: row.turbidity });

            sensorDataRealTime['acidity'] = sensorDataRealTime['acidity'] || [];
            sensorDataRealTime['acidity'].push({ date: row.date, value: row.acidity });

            sensorDataRealTime['conductivity'] = sensorDataRealTime['conductivity'] || [];
            sensorDataRealTime['conductivity'].push({ date: row.date, value: row.conductivity });

            sensorDataRealTime['trp'] = sensorDataRealTime['trp'] || [];
            sensorDataRealTime['trp'].push({ date: row.date, value: row.trp });

            sensorDataRealTime['bod'] = sensorDataRealTime['bod'] || [];
            sensorDataRealTime['bod'].push({ date: row.date, value: row.bod });

            sensorDataRealTime['cod'] = sensorDataRealTime['cod'] || [];
            sensorDataRealTime['cod'].push({ date: row.date, value: row.cod });

            sensorDataRealTime['no2'] = sensorDataRealTime['no2'] || [];
            sensorDataRealTime['no2'].push({ date: row.date, value: row.no2 });

            sensorDataRealTime['no3'] = sensorDataRealTime['no3'] || [];
            sensorDataRealTime['no3'].push({ date: row.date, value: row.no3 });
        });

        //console.log(sensorDataRealTime);

    await new Promise(res => setTimeout(res, 60 * 1000)); // 1 minute delay
    }})();



app.get('/sensor_data_hs', (req,res) => {
    res.json(sensorDataHistorical);
});
app.get('/sensor_data_rt', (req,res) => {
    res.json(sensorDataRealTime);
});

app.listen(port, () => {

    console.log(`Server running on port ${port}`)
});
