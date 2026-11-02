import { configureStore } from '@reduxjs/toolkit';
import cities from './citiesSlice';
import forecast from './forecastSlice';
import favorites from './favoritesSlice';
import settings from './settingsSlice';

export const store = configureStore({
  reducer: { cities, forecast, favorites, settings },
});
