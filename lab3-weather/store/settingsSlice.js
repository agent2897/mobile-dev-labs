import { createSlice } from '@reduxjs/toolkit';

const settingsSlice = createSlice({
  name: 'settings',
  initialState: { unit: 'celsius' },
  reducers: {
    setUnit: (state, action) => {
      state.unit = action.payload;
    },
  },
});

export const { setUnit } = settingsSlice.actions;
export default settingsSlice.reducer;
