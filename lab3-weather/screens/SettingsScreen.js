import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { Ionicons } from '@expo/vector-icons';
import { setUnit } from '../store/settingsSlice';
import { clearFavorites } from '../store/favoritesSlice';

const UNITS = [
  { value: 'celsius', label: 'Цельсій (°C)' },
  { value: 'fahrenheit', label: 'Фаренгейт (°F)' },
];

export default function SettingsScreen() {
  const dispatch = useDispatch();
  const unit = useSelector((s) => s.settings.unit);
  const favCount = useSelector((s) => s.favorites.length);

  return (
    <View style={styles.container}>
      <Text style={styles.section}>Одиниці температури</Text>
      <View style={styles.card}>
        {UNITS.map((u) => (
          <TouchableOpacity key={u.value} style={styles.option} onPress={() => dispatch(setUnit(u.value))}>
            <Text style={styles.label}>{u.label}</Text>
            <Ionicons
              name={unit === u.value ? 'radio-button-on' : 'radio-button-off'}
              size={22}
              color="#4a90e2"
            />
          </TouchableOpacity>
        ))}
      </View>
      <Text style={styles.section}>Обране</Text>
      <View style={styles.card}>
        <TouchableOpacity style={styles.option} onPress={() => dispatch(clearFavorites())}>
          <Text style={[styles.label, { color: '#d9534f' }]}>Очистити обране ({favCount})</Text>
          <Ionicons name="trash-outline" size={22} color="#d9534f" />
        </TouchableOpacity>
      </View>
      <Text style={styles.footer}>Дані: Open-Meteo.com</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#eef3f9', padding: 12 },
  section: { color: '#888', fontSize: 13, marginTop: 16, marginBottom: 6, marginLeft: 4 },
  card: { backgroundColor: '#fff', borderRadius: 12 },
  option: {
    flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center',
    padding: 16, borderBottomWidth: StyleSheet.hairlineWidth, borderBottomColor: '#ddd',
  },
  label: { fontSize: 16, color: '#222' },
  footer: { textAlign: 'center', color: '#aaa', marginTop: 30 },
});
