// Open-Meteo — безкоштовний API погоди, ключ не потрібен
const GEO = 'https://geocoding-api.open-meteo.com/v1/search';
const FORECAST = 'https://api.open-meteo.com/v1/forecast';

// Пошук міст за назвою
export async function searchCities(name) {
  const res = await fetch(`${GEO}?name=${encodeURIComponent(name)}&count=15&language=uk`);
  if (!res.ok) throw new Error('Помилка мережі');
  const json = await res.json();
  return (json.results || []).map((c) => ({
    id: c.id,
    name: c.name,
    country: c.country,
    region: c.admin1,
    lat: c.latitude,
    lon: c.longitude,
  }));
}

// Поточна погода та прогноз на 7 днів
export async function getForecast(city, unit) {
  const params = [
    `latitude=${city.lat}`,
    `longitude=${city.lon}`,
    'current=temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,weather_code',
    'daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max',
    `temperature_unit=${unit}`,
    'timezone=auto',
  ].join('&');
  const res = await fetch(`${FORECAST}?${params}`);
  if (!res.ok) throw new Error('Помилка мережі');
  return res.json();
}
