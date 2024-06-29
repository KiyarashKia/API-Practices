document.addEventListener('DOMContentLoaded', (event) => {
    // Check if the browser supports geolocation
    if (navigator.geolocation) {
        // Geo Location API function usage in addition to getWeather custom function to determine user's spot and getting weather info
        navigator.geolocation.getCurrentPosition(getWeather);
    } else {
        alert("Geolocation is not supported by this browser.");
    }

    document.getElementById('searchBtn').addEventListener('click', () => {
        const city = document.getElementById('cityInput').value;
        getWeatherByCity(city);
    });
});

const apiK ='92f004df3786852b49c3328caf61fba4';

function getWeather(position) {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;
    fetch(`https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${apiK}`)
        .then(response => response.json())
        .then(data => displayWeather(data))
        .catch(error => console.error('Error:', error));
}

function getWeatherByCity(city) {
    city = city.trim().replace(/\s+/g, ' ');
    fetch(`https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiK}&units=metric`) // Fetching data in celsius
    .then(response => response.json())
    .then(data => displayWeather(data))
    .catch(error => console.error('Error:', error));
}


function displayWeather(data) {
    const weatherInfo = document.getElementById('weatherInfo');
    weatherInfo.innerHTML = `
        <div class="card">
            <div class="card-body">
                <h2 class="card-title">${data.name}, ${data.sys.country}</h2>
                <img src="http://openweathermap.org/images/flags/${data.sys.country.toLowerCase()}.png" alt="Country Flag">
                <p class="card-text">Weather: ${data.weather[0].description}</p>
                <p class="card-text">Temperature: ${data.main.temp}°C</p>
                <p class="card-text">Wind Speed: ${data.wind.speed} m/s</p>
                <p class="card-text">Humidity: ${data.main.humidity}%</p>
                <p class="card-text">Pressure: ${data.main.pressure} hPa</p>
                <p class="card-text">Sunrise: ${new Date(data.sys.sunrise * 1000).toLocaleTimeString()}</p>
                <p class="card-text">Sunset: ${new Date(data.sys.sunset * 1000).toLocaleTimeString()}</p>
            </div>
        </div>
    `;
}


function displayError(message) {
    const weatherInfo = document.getElementById('weatherInfo');
    weatherInfo.innerHTML = `<p class="text-danger">${message}</p>`;
}