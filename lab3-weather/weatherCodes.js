// Коди погоди WMO -> опис та іконка Ionicons
const codes = {
  0: ['Ясно', 'sunny'],
  1: ['Переважно ясно', 'partly-sunny'],
  2: ['Мінлива хмарність', 'partly-sunny'],
  3: ['Хмарно', 'cloudy'],
  45: ['Туман', 'cloudy'],
  48: ['Туман з інеєм', 'cloudy'],
  51: ['Мряка', 'rainy'],
  53: ['Мряка', 'rainy'],
  55: ['Сильна мряка', 'rainy'],
  61: ['Невеликий дощ', 'rainy'],
  63: ['Дощ', 'rainy'],
  65: ['Сильний дощ', 'rainy'],
  71: ['Невеликий сніг', 'snow'],
  73: ['Сніг', 'snow'],
  75: ['Сильний сніг', 'snow'],
  80: ['Злива', 'rainy'],
  81: ['Злива', 'rainy'],
  82: ['Сильна злива', 'thunderstorm'],
  95: ['Гроза', 'thunderstorm'],
  96: ['Гроза з градом', 'thunderstorm'],
  99: ['Гроза з градом', 'thunderstorm'],
};

export const describe = (code) => {
  const [text, icon] = codes[code] || ['Невідомо', 'help-circle'];
  return { text, icon };
};
