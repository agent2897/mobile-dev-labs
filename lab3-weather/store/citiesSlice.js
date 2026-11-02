import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { searchCities } from '../api';

export const findCities = createAsyncThunk('cities/find', (name) => searchCities(name));

const citiesSlice = createSlice({
  name: 'cities',
  initialState: { results: [], status: 'idle', error: null },
  reducers: {
    clearResults: (state) => {
      state.results = [];
      state.status = 'idle';
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(findCities.pending, (state) => {
        state.status = 'loading';
        state.error = null;
      })
      .addCase(findCities.fulfilled, (state, action) => {
        state.status = 'done';
        state.results = action.payload;
      })
      .addCase(findCities.rejected, (state, action) => {
        state.status = 'error';
        state.error = action.error.message;
      });
  },
});

export const { clearResults } = citiesSlice.actions;
export default citiesSlice.reducer;
