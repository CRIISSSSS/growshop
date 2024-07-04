
const APIKey = "1dd91bd7bcae6a11f02e318197546bc5";
const queryURL = `http://api.openweathermap.org/data/2.5/weather?q=Concepcion&appid=${APIKey}&lang=es`;
const a = fetch(queryURL)
.then(response => response.json())
.then(data => {
    const weatherInfo = document.getElementById("weatherInfo");
    weatherInfo.innerHTML = `<h2>Clima en Concepción</h2>
                            <p>Temperatura: ${data.main.temp} °C</p>
                            <p>Descripción: ${data.weather[0].description}</p>`
})
.catch(error => {
    console.error('Error al obtener el clima: ', error);
    const weatherInfo = document.getElementById("weatherInfo");
    weatherInfo.innerHTML = `<p>Error al obtener el clima. Por favor, intente de nuevo más tarde.</p>`;
});

