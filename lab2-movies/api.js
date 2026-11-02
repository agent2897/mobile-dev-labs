import { movies } from './mockData';

// Безкоштовний ключ можна отримати на http://www.omdbapi.com/apikey.aspx
// Якщо ключ порожній, використовуються макетні дані з mockData.js
const API_KEY = '';
const BASE = 'https://www.omdbapi.com/';
const PAGE_SIZE = 10;

// Пошук фільмів: повертає { results, total }
export async function searchMovies(query, page = 1) {
  if (!API_KEY) {
    const found = movies.filter((m) => m.Title.toLowerCase().includes(query.toLowerCase()));
    return { results: found.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE), total: found.length };
  }
  const res = await fetch(`${BASE}?apikey=${API_KEY}&s=${encodeURIComponent(query)}&page=${page}`);
  const json = await res.json();
  if (json.Response === 'False') return { results: [], total: 0 };
  return { results: json.Search, total: Number(json.totalResults) };
}

// Детальна інформація про фільм за imdbID
export async function getMovie(id) {
  if (!API_KEY) return movies.find((m) => m.imdbID === id);
  const res = await fetch(`${BASE}?apikey=${API_KEY}&i=${id}&plot=full`);
  return res.json();
}
