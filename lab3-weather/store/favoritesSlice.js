import { createSlice } from '@reduxjs/toolkit';

const favoritesSlice = createSlice({
  name: 'favorites',
  initialState: [],
  reducers: {
    toggleFavorite: (state, action) => {
      const i = state.findIndex((c) => c.id === action.payload.id);
      if (i >= 0) state.splice(i, 1);
      else state.push(action.payload);
    },
    clearFavorites: () => [],
  },
});

export const { toggleFavorite, clearFavorites } = favoritesSlice.actions;
export default favoritesSlice.reducer;
