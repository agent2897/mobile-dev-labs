import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import { ScrollView, View, Text, Image, ActivityIndicator, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { getMovie } from '../api';

const Field = ({ icon, label, value }) => (
  <View style={styles.field}>
    <Ionicons name={icon} size={18} color="#f5c518" />
    <Text style={styles.label}>{label}: </Text>
    <Text style={styles.value}>{value}</Text>
  </View>
);

Field.propTypes = {
  icon: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  value: PropTypes.string,
};

export default function DetailsScreen({ route }) {
  const [movie, setMovie] = useState(null);

  useEffect(() => {
    getMovie(route.params.id).then(setMovie);
  }, [route.params.id]);

  if (!movie) return <ActivityIndicator style={styles.container} color="#f5c518" />;

  return (
    <ScrollView style={styles.container} contentContainerStyle={{ padding: 16 }}>
      {movie.Poster !== 'N/A' ? (
        <Image source={{ uri: movie.Poster }} style={styles.poster} />
      ) : (
        <View style={[styles.poster, styles.noPoster]}>
          <Ionicons name="film-outline" size={64} color="#666" />
        </View>
      )}
      <Text style={styles.title}>{movie.Title}</Text>
      <Field icon="calendar-outline" label="Рік" value={movie.Year} />
      <Field icon="star" label="Рейтинг IMDb" value={movie.imdbRating} />
      <Field icon="time-outline" label="Тривалість" value={movie.Runtime} />
      <Field icon="pricetags-outline" label="Жанр" value={movie.Genre} />
      <Field icon="person-outline" label="Режисер" value={movie.Director} />
      <Field icon="people-outline" label="Актори" value={movie.Actors} />
      <Text style={styles.plot}>{movie.Plot}</Text>
    </ScrollView>
  );
}

DetailsScreen.propTypes = {
  route: PropTypes.shape({ params: PropTypes.shape({ id: PropTypes.string.isRequired }) }).isRequired,
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#141414' },
  poster: { width: 200, height: 296, alignSelf: 'center', borderRadius: 8, marginBottom: 16 },
  noPoster: { backgroundColor: '#2a2a2a', alignItems: 'center', justifyContent: 'center' },
  title: { color: '#fff', fontSize: 22, fontWeight: 'bold', textAlign: 'center', marginBottom: 14 },
  field: { flexDirection: 'row', alignItems: 'flex-start', marginVertical: 4, flexWrap: 'wrap' },
  label: { color: '#aaa', fontSize: 15, marginLeft: 8 },
  value: { color: '#fff', fontSize: 15, flexShrink: 1 },
  plot: { color: '#ddd', fontSize: 15, lineHeight: 22, marginTop: 14 },
});
