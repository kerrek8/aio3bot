city_coords = {
    'strej': {
        'latitude': 60.72411,
        'longitude': 77.58138,
    },
    'tymen': {
        'latitude': 57.1522,
        'longitude': 65.5272,
    }
}


async def WeatherEndpointCurrent():
    WeatherEndpoinCurrent = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&units=metric&lang=ru"
    return WeatherEndpoinCurrent


async def WeatherEndpointDays():
    WeatherEndpoinDays = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&cnt={}&appid={}&units=metric&lang=ru"
    return WeatherEndpoinDays
