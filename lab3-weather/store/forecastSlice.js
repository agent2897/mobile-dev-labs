import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { getForecast } from '../api';

// Одиниці температури беруться зі стану налаштувань
export const loadForecast = createAsyncThunk('forecast/load', (city, { getState }) =>
  getForecast(city, getState().settings.unit)
);

const forecastSlice = createSlice({
  name: 'forecast',
  initialState: { byCity: {}, status: {} },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(loadForecast.pending, (state, action) => {
        state.status[action.meta.arg.id] = 'loading';
      })
      .addCase(loadForecast.fulfilled, (state, action) => {
        state.status[action.meta.arg.id] = 'done';
        state.byCity[action.meta.arg.id] = action.payload;
      })
      .addCase(loadForecast.rejected, (state, action) => {
        state.status[action.meta.arg.id] = 'error';
      });
  },
});

export default forecastSlice.reducer;
