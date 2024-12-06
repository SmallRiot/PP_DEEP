import { createSlice } from "@reduxjs/toolkit";

const radioSlice = createSlice({
  name: "radio",
  initialState: {
    selectedOption: "",
    freeze: false,
  },
  reducers: {
    selectOption: (state, action) => {
      if (state.selectedOption !== action.payload) {
        state.selectedOption = action.payload;
      }
    },
    setFreeze: (state, action) => {
      state.freeze = action.payload;
    },
  },
});

export const { selectOption, setFreeze } = radioSlice.actions;
export default radioSlice.reducer;
