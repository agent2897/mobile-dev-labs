import React, { useEffect, useLayoutEffect } from 'react';
import PropTypes from 'prop-types';
import { ScrollView, View, Text, ActivityIndicator, TouchableOpacity, StyleSheet } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { Ionicons } from '@expo/vector-icons';
import { loadForecast } from '../store/forecastSlice';
import { toggleFavorite } from '../store/favoritesSlice';
import { describe } from '../weatherCodes';

const DAYS = ['Нд', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'];

export default function WeatherScreen({ route, navigation }) {
  const { city } = route.params;
  const dispatch = useDispatch();
  const data = useSelector((s) => s.forecast.byCity[city.id]);
  const status = useSelector((s) => s.forecast.status[city.id]);
  const unit = useSelector((s) => s.settings.unit);
  const isFav = useSelector((s) => s.favorites.some((c) => c.id === city.id));

  useEffect(() => {
    dispatch(loadForecast(city));
  }, [city.id, unit]);

  // Кнопка «обране» в заголовку стекового навігатора
  useLayoutEffect(() => {
    navigation.setOptions({
      title: city.name,
      headerRight: () => (
        <TouchableOpacity onPress={() => dispatch(toggleFavorite(city))} style={{ marginRight: 16 }}>
          <Ionicons name={isFav ? 'star' : 'star-outline'} size={24} color="#fff" />
        </TouchableOpacity>
      ),
    });
  }, [isFav]);

  if (status === 'error') return <Text style={styles.msg}>Не вдалося завантажити прогноз</Text>;
  if (!data) return <ActivityIndicator style={{ marginTop: 40 }} color="#4a90e2" />;

  const cur = data.current;
  const now = describe(cur.weather_code);
  const deg = unit === 'celsius' ? '°C' : '°F';

  return (
    <ScrollView style={styles.container} contentContainerStyle={{ padding: 16 }}>
      <View style={styles.card}>
        <Ionicons name={now.icon} size={80} color="#f5a623" />
        <Text style={styles.temp}>{Math.round(cur.temperature_2m)}{deg}</Text>
        <Text style={styles.desc}>{now.text}</Text>
        <Text style={styles.sub}>{[city.region, city.country].filter(Boolean).join(', ')}</Text>
        <View style={styles.stats}>
          <Stat icon="thermometer-outline" label="Відчувається" value={`${Math.round(cur.apparent_temperature)}${deg}`} />
          <Stat icon="water-outline" label="Вологість" value={`${cur.relative_humidity_2m}%`} />
          <Stat icon="flag-outline" label="Вітер" value={`${cur.wind_speed_10m} км/г`} />
        </View>
      </View>
      <Text style={styles.section}>Прогноз на 7 днів</Text>
      {data.daily.time.map((day, i) => {
        const d = describe(data.daily.weather_code[i]);
        return (
          <View key={day} style={styles.dayRow}>
            <Text style={styles.dayName}>{i === 0 ? 'Сьогодні' : DAYS[new Date(day).getDay()]}</Text>
            <Ionicons name={d.icon} size={22} color="#4a90e2" />
            <Text style={styles.rain}>{data.daily.precipitation_probability_max[i]}%</Text>
            <Text style={styles.range}>
              {Math.round(data.daily.temperature_2m_min[i])}° / {Math.round(data.daily.temperature_2m_max[i])}°
            </Text>
          </View>
        );
      })}
    </ScrollView>
  );
}

const Stat = ({ icon, label, value }) => (
  <View style={styles.stat}>
    <Ionicons name={icon} size={20} color="#4a90e2" />
    <Text style={styles.statVal}>{value}</Text>
    <Text style={styles.statLabel}>{label}</Text>
  </View>
);

Stat.propTypes = {
  icon: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  value: PropTypes.string.isRequired,
};

WeatherScreen.propTypes = {
  route: PropTypes.shape({ params: PropTypes.shape({ city: PropTypes.object.isRequired }) }).isRequired,
  navigation: PropTypes.shape({ setOptions: PropTypes.func.isRequired }).isRequired,
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#eef3f9' },
  card: { backgroundColor: '#fff', borderRadius: 16, padding: 20, alignItems: 'center' },
  temp: { fontSize: 56, fontWeight: '300', color: '#222' },
  desc: { fontSize: 20, color: '#444' },
  sub: { fontSize: 14, color: '#888', marginTop: 4 },
  stats: { flexDirection: 'row', marginTop: 18, width: '100%', justifyContent: 'space-around' },
  stat: { alignItems: 'center' },
  statVal: { fontSize: 16, fontWeight: '600', marginTop: 4, color: '#222' },
  statLabel: { fontSize: 12, color: '#888' },
  section: { fontSize: 18, fontWeight: '600', marginTop: 20, marginBottom: 8, color: '#222' },
  dayRow: {
    flexDirection: 'row', alignItems: 'center', backgroundColor: '#fff',
    padding: 12, borderRadius: 10, marginVertical: 3,
  },
  dayName: { width: 80, fontSize: 15, color: '#222' },
  rain: { width: 50, marginLeft: 10, color: '#4a90e2', fontSize: 13 },
  range: { flex: 1, textAlign: 'right', fontSize: 15, color: '#222' },
  msg: { textAlign: 'center', color: '#888', marginTop: 40 },
});
