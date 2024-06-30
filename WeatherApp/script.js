document.addEventListener('DOMContentLoaded', (event) => {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(getWeather);
    } else {
        alert("Geolocation is not supported by this browser.");
    }

    document.getElementById('searchBtn').addEventListener('click', () => {
        const city = document.getElementById('cityInput').value;
        getWeatherByCity(city);

        document.getElementById('cityInput').addEventListener('keypress', (event) => {
            if (event.key === 'Enter') {
                event.preventDefault();
                document.getElementById('searchBtn').click();
            }
        });
    });
});

const apikey = '92f004df3786852b49c3328caf61fba4';

function getWeather(position) {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;
    fetch(`https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${apikey}&units=metric`)
        .then(response => response.json())
        .then(data => displayWeather([data]))
        .catch(error => console.error('Error:', error));
}

function getWeatherByCity(city) {
    city = city.trim().replace(/\s+/g, ' ');
    fetch(`https://api.openweathermap.org/data/2.5/find?q=${city}&appid=${apikey}&units=metric`)
        .then(response => response.json())
        .then(data => {
            if (data.cod === '404' || data.count === 0) {
                displayError('City not found');
            } else {
                displayWeather(data.list);
            }
        })
        .catch(error => console.error('Error:', error));
}

function displayWeather(dataArray) {
    const weatherInfo = document.getElementById('weatherInfo');
    weatherInfo.innerHTML = '';

    dataArray.forEach((data, index) => {
        const countryCode = data.sys.country.toUpperCase();
        const card = document.createElement('div');
        card.className = 'col-sm-3 mb-4';
        card.innerHTML = `
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">${data.name}, ${data.sys.country}</h5>
                    <img src="https://flagsapi.com/${countryCode}/shiny/64.png" alt="Country Flag" class="mb-2">
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
        weatherInfo.appendChild(card);

        // Delay the animation for each card
        setTimeout(() => {
            card.querySelector('.card').classList.add('show');
        }, 100 * index);
    });
}

function displayError(message) {
    const weatherInfo = document.getElementById('weatherInfo');
    weatherInfo.innerHTML = `<p class="text-danger">${message}</p>`;
}
