import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { View, TextInput, FlatList, Text, ActivityIndicator, TouchableOpacity, StyleSheet } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { Ionicons } from '@expo/vector-icons';
import { findCities, clearResults } from '../store/citiesSlice';
import CityRow from '../components/CityRow';

export default function SearchScreen({ navigation }) {
  const [query, setQuery] = useState('');
  const dispatch = useDispatch();
  const { results, status, error } = useSelector((s) => s.cities);

  const submit = () => {
    if (query.trim().length >= 2) dispatch(findCities(query.trim()));
  };

  return (
    <View style={styles.container}>
      <View style={styles.searchBox}>
        <Ionicons name="search" size={20} color="#888" />
        <TextInput
          style={styles.input}
          placeholder="Введіть місто"
          value={query}
          onChangeText={(t) => {
            setQuery(t);
            if (!t) dispatch(clearResults());
          }}
          onSubmitEditing={submit}
          returnKeyType="search"
        />
        <TouchableOpacity style={styles.btn} onPress={submit}>
          <Text style={styles.btnText}>Знайти</Text>
        </TouchableOpacity>
      </View>
      {status === 'loading' && <ActivityIndicator style={{ margin: 20 }} color="#4a90e2" />}
      {status === 'error' && <Text style={styles.msg}>{error}</Text>}
      {status === 'done' && results.length === 0 && <Text style={styles.msg}>Місто не знайдено</Text>}
      {status === 'idle' && <Text style={styles.msg}>Знайдіть місто, щоб переглянути погоду</Text>}
      <FlatList
        style={{ flex: 1 }}
        data={results}
        keyExtractor={(c) => String(c.id)}
        renderItem={({ item }) => (
          <CityRow city={item} onPress={() => navigation.navigate('Weather', { city: item })} />
        )}
      />
    </View>
  );
}

SearchScreen.propTypes = {
  navigation: PropTypes.shape({ navigate: PropTypes.func.isRequired }).isRequired,
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#eef3f9' },
  searchBox: {
    flexDirection: 'row', alignItems: 'center', backgroundColor: '#fff',
    margin: 12, paddingLeft: 12, borderRadius: 12, overflow: 'hidden',
  },
  input: { flex: 1, fontSize: 16, paddingVertical: 12, marginLeft: 8 },
  btn: { backgroundColor: '#4a90e2', paddingHorizontal: 16, paddingVertical: 14 },
  btnText: { color: '#fff', fontWeight: '600', fontSize: 15 },
  msg: { textAlign: 'center', color: '#888', marginTop: 24, fontSize: 15 },
});
