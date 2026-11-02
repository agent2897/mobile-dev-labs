import React from 'react';
import PropTypes from 'prop-types';
import { TouchableOpacity, View, Text, Image, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

// Рядок списку результатів пошуку
export default function MovieRow({ movie, onPress }) {
  return (
    <TouchableOpacity style={styles.row} onPress={onPress}>
      {movie.Poster && movie.Poster !== 'N/A' ? (
        <Image source={{ uri: movie.Poster }} style={styles.poster} />
      ) : (
        <View style={[styles.poster, styles.noPoster]}>
          <Ionicons name="film-outline" size={28} color="#888" />
        </View>
      )}
      <View style={styles.info}>
        <Text style={styles.title} numberOfLines={2}>{movie.Title}</Text>
        <Text style={styles.sub}>{movie.Year} · {movie.Type}</Text>
      </View>
      <Ionicons name="chevron-forward" size={22} color="#666" />
    </TouchableOpacity>
  );
}

MovieRow.propTypes = {
  movie: PropTypes.shape({
    Title: PropTypes.string.isRequired,
    Year: PropTypes.string,
    Type: PropTypes.string,
    Poster: PropTypes.string,
  }).isRequired,
  onPress: PropTypes.func.isRequired,
};

const styles = StyleSheet.create({
  row: {
    flexDirection: 'row', alignItems: 'center', padding: 10,
    borderBottomWidth: 1, borderBottomColor: '#2a2a2a',
  },
  poster: { width: 50, height: 74, borderRadius: 4 },
  noPoster: { backgroundColor: '#2a2a2a', alignItems: 'center', justifyContent: 'center' },
  info: { flex: 1, marginLeft: 12 },
  title: { color: '#fff', fontSize: 16, fontWeight: '600' },
  sub: { color: '#aaa', fontSize: 13, marginTop: 4 },
});
