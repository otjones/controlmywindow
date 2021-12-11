const { response } = require("express");
const fs = require("fs");
const request = require("request");
const fetch = require("node-fetch");
const { spawn } = require("child_process");

module.exports = {
  confirm: function () {
    console.log("Imported worker.js");
  },
  arrayLoad: function (loc) {
    return JSON.parse(fs.readFileSync(loc, "utf8"));
  },
  arrayAddLine: function (entry, loc) {
    var array = JSON.parse(fs.readFileSync(loc, "utf8"));
    return array.concat([entry]);
  },
  arrayWrite: function (array, loc) {
    fs.writeFileSync(loc, JSON.stringify(array));
  },
  createEntry: function () {
    let date_ob = new Date();
    let month = ("0" + (date_ob.getMonth() + 1)).slice(-2);
    let date = ("0" + date_ob.getDate()).slice(-2);
    let hours = ("0" + (date_ob.getHours() + 1)).slice(-2);
    let minutes = ("0" + (date_ob.getMinutes() + 1)).slice(-2);
    let seconds = ("0" + (date_ob.getSeconds() + 1)).slice(-2);
    const time = [month, date, hours, minutes, seconds];
    return { time: time };
  },
  addWeather: async function () {
    const response = await fetch(
      "https://api.openweathermap.org/data/2.5/onecall?lat=51.475706&lon=-0.206082&exclude=daily,hourly,alerts&appid=########################"
    );
    const data = await response.json();
    const packet = {};
    pRain = 0;
    for (let i = 0; i < 3; i++) {
      pRain += data.minutely[i].precipitation;
    }
    packet["temp"] = parseFloat(data.current.temp - 273.15).toFixed(2);
    packet["hum"] = parseFloat(data.current.humidity).toFixed(2);
    packet["wind"] = parseFloat(data.current.wind_gust).toFixed(2);
    packet["rain"] = parseFloat(pRain).toFixed(2);
    return packet;
  },

  addLocal: async function () {
    const packet = {};
    const childPython = spawn("python", ["./src/weather.py"]);
    childPython.stderr.on("data", (data) => {
      //console.log(`${data}`)
    });
    childPython.stdout.on("data", (data) => {
      //console.log(`${data}`)
      packet["temp"] = parseFloat(
        `${data}`.split("(")[1].split(",")[0]
      ).toFixed(2);
      packet["hum"] = parseFloat(`${data}`.split(" ")[1].split(")")[0]).toFixed(
        2
      );
    });
    return new Promise((resolve) =>
      childPython.on("exit", () => {
        resolve(packet);
      })
    );
  },
};
