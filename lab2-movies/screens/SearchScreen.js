import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { View, TextInput, FlatList, Text, ActivityIndicator, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { searchMovies } from '../api';
import MovieRow from '../components/MovieRow';

export default function SearchScreen({ navigation }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);

  const search = async (text) => {
    setQuery(text);
    if (text.trim().length < 3) {
      setResults([]);
      setTotal(0);
      return;
    }
    setLoading(true);
    const data = await searchMovies(text.trim(), 1);
    setResults(data.results);
    setTotal(data.total);
    setPage(1);
    setLoading(false);
  };

  // Довантаження наступної сторінки — показ понад 10 результатів
  const loadMore = async () => {
    if (loading || results.length >= total) return;
    setLoading(true);
    const data = await searchMovies(query.trim(), page + 1);
    setResults((r) => [...r, ...data.results]);
    setPage(page + 1);
    setLoading(false);
  };

  return (
    <View style={styles.container}>
      <View style={styles.searchBox}>
        <Ionicons name="search" size={20} color="#aaa" />
        <TextInput
          style={styles.input}
          placeholder="Назва фільму (мін. 3 символи)"
          placeholderTextColor="#777"
          value={query}
          onChangeText={search}
        />
      </View>
      {total > 0 && <Text style={styles.count}>Знайдено: {total}</Text>}
      <FlatList
        style={styles.list}
        data={results}
        keyExtractor={(item) => item.imdbID}
        renderItem={({ item }) => (
          <MovieRow movie={item} onPress={() => navigation.navigate('Details', { id: item.imdbID, title: item.Title })} />
        )}
        onEndReached={loadMore}
        onEndReachedThreshold={0.5}
        ListFooterComponent={loading ? <ActivityIndicator style={{ margin: 16 }} color="#f5c518" /> : null}
        ListEmptyComponent={!loading && query.length >= 3 ? <Text style={styles.empty}>Нічого не знайдено</Text> : null}
      />
    </View>
  );
}

SearchScreen.propTypes = {
  navigation: PropTypes.shape({ navigate: PropTypes.func.isRequired }).isRequired,
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#141414' },
  list: { flex: 1 },
  searchBox: {
    flexDirection: 'row', alignItems: 'center', backgroundColor: '#222',
    margin: 12, paddingHorizontal: 12, borderRadius: 10,
  },
  input: { flex: 1, color: '#fff', fontSize: 16, paddingVertical: 10, marginLeft: 8 },
  count: { color: '#aaa', marginHorizontal: 14, marginBottom: 4 },
  empty: { color: '#aaa', textAlign: 'center', marginTop: 30, fontSize: 16 },
});
