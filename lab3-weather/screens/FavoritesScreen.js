import React from 'react';
import PropTypes from 'prop-types';
import { View, FlatList, Text, StyleSheet } from 'react-native';
import { useSelector } from 'react-redux';
import { Ionicons } from '@expo/vector-icons';
import CityRow from '../components/CityRow';

export default function FavoritesScreen({ navigation }) {
  const favorites = useSelector((s) => s.favorites);

  if (favorites.length === 0) {
    return (
      <View style={[styles.container, styles.empty]}>
        <Ionicons name="star-outline" size={60} color="#bbb" />
        <Text style={styles.msg}>Немає обраних міст.{'\n'}Натисніть ☆ біля міста, щоб додати.</Text>
      </View>
    );
  }

  return (
    <FlatList
      style={styles.container}
      contentContainerStyle={{ paddingVertical: 8 }}
      data={favorites}
      keyExtractor={(c) => String(c.id)}
      renderItem={({ item }) => (
        <CityRow city={item} onPress={() => navigation.navigate('Weather', { city: item })} />
      )}
    />
  );
}

FavoritesScreen.propTypes = {
  navigation: PropTypes.shape({ navigate: PropTypes.func.isRequired }).isRequired,
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#eef3f9' },
  empty: { alignItems: 'center', justifyContent: 'center' },
  msg: { textAlign: 'center', color: '#888', marginTop: 12, fontSize: 15, lineHeight: 22 },
});
