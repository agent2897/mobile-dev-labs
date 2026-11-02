import React from 'react';
import PropTypes from 'prop-types';
import { TouchableOpacity, View, Text, StyleSheet } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { Ionicons } from '@expo/vector-icons';
import { toggleFavorite } from '../store/favoritesSlice';

// Рядок міста зі зіркою «обране»
export default function CityRow({ city, onPress }) {
  const dispatch = useDispatch();
  const isFav = useSelector((s) => s.favorites.some((c) => c.id === city.id));

  return (
    <TouchableOpacity style={styles.row} onPress={onPress}>
      <Ionicons name="location-outline" size={24} color="#4a90e2" />
      <View style={styles.info}>
        <Text style={styles.name}>{city.name}</Text>
        <Text style={styles.sub}>{[city.region, city.country].filter(Boolean).join(', ')}</Text>
      </View>
      <TouchableOpacity onPress={() => dispatch(toggleFavorite(city))} hitSlop={10}>
        <Ionicons name={isFav ? 'star' : 'star-outline'} size={24} color="#f5a623" />
      </TouchableOpacity>
    </TouchableOpacity>
  );
}

CityRow.propTypes = {
  city: PropTypes.shape({
    id: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired,
    region: PropTypes.string,
    country: PropTypes.string,
  }).isRequired,
  onPress: PropTypes.func.isRequired,
};

const styles = StyleSheet.create({
  row: {
    flexDirection: 'row', alignItems: 'center', backgroundColor: '#fff',
    marginHorizontal: 12, marginVertical: 5, padding: 14, borderRadius: 12,
  },
  info: { flex: 1, marginLeft: 12 },
  name: { fontSize: 17, fontWeight: '600', color: '#222' },
  sub: { fontSize: 13, color: '#888', marginTop: 2 },
});
