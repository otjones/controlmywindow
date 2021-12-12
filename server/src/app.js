const fetch = require("node-fetch");
const express = require("express");
const app = express();
app.use(express.json());

var cors = require("cors");
app.use(cors());

const tools = require("./worker.js");
tools.confirm();
tools.arrayWrite([], "./data/log.json");

const { spawn } = require("child_process");

spawn("python", ["./src/endStop.py"]);

var windowStatus = "";

setInterval(async function () {
  var entry = tools.createEntry();
  console.log("fetching weather");
  entry["weather"] = await tools.addWeather();
  console.log("fetching local");
  entry["local"] = await tools.addLocal();
  tools.arrayWrite(
    tools.arrayAddLine(entry, "./data/log.json"),
    "./data/log.json"
  );

  i_temp = entry["local"].temp;
  rain = entry["weather"].rain;
  wind = entry["weather"].wind;

  if (
    rain < 1 &&
    wind < 3 &&
    i_temp > 20 &&
    windowStatus != "Manually Stopped"
  ) {
    const childPython = spawn("python", ["./src/motorFORWARD.py"]);
    windowStatus = "Open";
  } else {
    const childPython = spawn("python", ["./src/motorBACKWARD.py"]);
    windowStatus = "Closed";
  }
}, 1000 * 60 * 2);

app.get("/", (req, res) => {
  res.send("Hello World");
  console.log("root request");
});

app.get("/pull", (req, res) => {
  res.send(tools.arrayLoad("./data/log.json"));
  console.log("request recieved");
});

app.get("/open", (req, res) => {
  const childPython = spawn("python", ["./src/motorFORWARD.py"]);
  windowStatus = "Open";
  res.send([windowStatus]);
});

app.get("/close", (req, res) => {
  const childPython = spawn("python", ["./src/motorBACKWARD.py"]);
  windowStatus = "Closed";
  res.send([windowStatus]);
});

app.get("/stop", (req, res) => {
  const childPython = spawn("python", ["./src/motorSTOP.py"]);
  windowStatus = "Manually Stopped";
  res.send([windowStatus]);
});

app.get("/status", (req, res) => {
  res.send([windowStatus]);
});

app.post("/message", (req, res) => {
  response = req.body;
  res.send("got it");
  console.log(response);
  fetch("http://localhost:5000/message/" + response.message);
});

app.listen(3000, () => console.log("running in the 90s"));
