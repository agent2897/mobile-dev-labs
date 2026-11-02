// Макетні дані у форматі відповідей OMDb API
const titles = [
  ['Star Wars: Episode IV - A New Hope', '1977', 'George Lucas', 'Action, Adventure, Fantasy', '8.6'],
  ['Star Wars: Episode V - The Empire Strikes Back', '1980', 'Irvin Kershner', 'Action, Adventure, Fantasy', '8.7'],
  ['Star Wars: Episode VI - Return of the Jedi', '1983', 'Richard Marquand', 'Action, Adventure, Fantasy', '8.3'],
  ['Star Wars: Episode I - The Phantom Menace', '1999', 'George Lucas', 'Action, Adventure, Fantasy', '6.5'],
  ['Star Wars: Episode II - Attack of the Clones', '2002', 'George Lucas', 'Action, Adventure, Fantasy', '6.6'],
  ['Star Wars: Episode III - Revenge of the Sith', '2005', 'George Lucas', 'Action, Adventure, Fantasy', '7.6'],
  ['Star Wars: Episode VII - The Force Awakens', '2015', 'J.J. Abrams', 'Action, Adventure, Sci-Fi', '7.8'],
  ['Rogue One: A Star Wars Story', '2016', 'Gareth Edwards', 'Action, Adventure, Sci-Fi', '7.8'],
  ['Star Wars: Episode VIII - The Last Jedi', '2017', 'Rian Johnson', 'Action, Adventure, Fantasy', '6.9'],
  ['Solo: A Star Wars Story', '2018', 'Ron Howard', 'Action, Adventure, Sci-Fi', '6.9'],
  ['Star Wars: Episode IX - The Rise of Skywalker', '2019', 'J.J. Abrams', 'Action, Adventure, Fantasy', '6.4'],
  ['Star Wars: The Clone Wars', '2008', 'Dave Filoni', 'Animation, Action, Adventure', '5.9'],
  ['The Mandalorian', '2019', 'Jon Favreau', 'Action, Adventure, Fantasy', '8.6'],
  ['Andor', '2022', 'Tony Gilroy', 'Action, Adventure, Drama', '8.4'],
  ['Star Wars: The Bad Batch', '2021', 'Dave Filoni', 'Animation, Action, Adventure', '7.8'],
];

export const movies = titles.map(([Title, Year, Director, Genre, imdbRating], i) => ({
  Title,
  Year,
  imdbID: `tt${String(1000000 + i)}`,
  Type: i >= 11 ? 'series' : 'movie',
  Poster: 'N/A',
  Director,
  Genre,
  imdbRating,
  Runtime: `${110 + i * 3} min`,
  Actors: 'Mark Hamill, Harrison Ford, Carrie Fisher',
  Plot: `${Title} — фільм із всесвіту «Зоряних війн», який продовжує епічну історію боротьби між Імперією та Повстанцями.`,
}));
