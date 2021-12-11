function plotAll() {
  fetch("https://window.eu.ngrok.io/pull")
    .then((response) => {
      return response.json();
    })
    .then((json) => {
      const data = json;
      console.log(data);

      time = [];
      w_temp = [];
      w_hum = [];
      w_rain = [];
      w_wind = [];
      l_temp = [];
      l_hum = [];

      for (let i = 0; i < data.length; i++) {
        time[i] = data[i].time[2].toString() + ":" + data[i].time[3].toString();
        w_temp[i] = data[i].weather.temp;
        w_hum[i] = data[i].weather.hum;
        w_rain[i] = data[i].weather.rain;
        w_wind[i] = data[i].weather.wind;
        l_temp[i] = data[i].local.temp;
        l_hum[i] = data[i].local.hum;
      }

      let temp_chart = document.getElementById("temp_chart");
      let tempChart = new Chart(temp_chart, {
        type: "line",
        data: {
          labels: time,
          datasets: [
            {
              label: "Outside",
              data: w_temp,
              backgroundColor: "blue",
              borderColor: "blue",
              color: "blue",
              cubicInterpolationMode: "monotone",
              tension: 0.4,
            },
            {
              label: "Inside",
              data: l_temp,
              backgroundColor: "red",
              borderColor: "red",
              color: "red",
            },
          ],
        },
        options: {
          scales: {
            y: {
              min: -10,
              max: 40,
            },
          },
        },
      });

      let hum_chart = document.getElementById("hum_chart");
      let humChart = new Chart(hum_chart, {
        type: "line",
        data: {
          labels: time,
          datasets: [
            {
              label: "Outside",
              data: w_hum,
              backgroundColor: "blue",
              borderColor: "blue",
              color: "blue",
              cubicInterpolationMode: "monotone",
              tension: 0.4,
            },
            {
              label: "Inside",
              data: l_hum,
              backgroundColor: "red",
              borderColor: "red",
              color: "red",
            },
          ],
        },
        options: {
          scales: {
            y: {
              min: 0,
              max: 100,
            },
          },
        },
      });

      let wind_chart = document.getElementById("wind_chart");
      let windChart = new Chart(wind_chart, {
        type: "line",
        data: {
          labels: time,
          datasets: [
            {
              label: "Outside",
              data: w_wind,
              backgroundColor: "blue",
              borderColor: "blue",
              color: "blue",
              cubicInterpolationMode: "monotone",
              tension: 0.4,
            },
          ],
        },
        options: {
          scales: {
            y: {
              min: 0,
              max: 40,
            },
          },
        },
      });

      let rain_chart = document.getElementById("rain_chart");
      let rainChart = new Chart(rain_chart, {
        type: "line",
        data: {
          labels: time,
          datasets: [
            {
              label: "Outside",
              data: w_rain,
              backgroundColor: "blue",
              borderColor: "blue",
              color: "blue",
              cubicInterpolationMode: "monotone",
              tension: 0.4,
            },
          ],
        },
        options: {
          scales: {
            y: {
              min: 0,
              max: 100,
            },
          },
        },
      });
    });
}

function openWindow() {
  fetch("https://window.eu.ngrok.io/open")
    .then((response) => {
      return response.json();
    })
    .then((json) => {
      const data = json;
      document.getElementById("status").innerHTML = data;
    });
}

function closeWindow() {
  fetch("https://window.eu.ngrok.io/close")
    .then((response) => {
      return response.json();
    })
    .then((json) => {
      const data = json;
      document.getElementById("status").innerHTML = data;
    });
}

function stopWindow() {
  fetch("https://window.eu.ngrok.io/stop")
    .then((response) => {
      return response.json();
    })
    .then((json) => {
      const data = json;
      document.getElementById("status").innerHTML = data;
    });
}

function getStatus() {
  fetch("https://window.eu.ngrok.io/status")
    .then((response) => {
      return response.json();
    })
    .then((json) => {
      const data = json;
      console.log(data);
      document.getElementById("status").innerHTML = data;
    });
}
