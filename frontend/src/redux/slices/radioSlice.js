import { createSlice } from "@reduxjs/toolkit";

const radioSlice = createSlice({
  name: "radio",
  initialState: {
    selectedOption: "",
  },
  reducers: {
    selectOption: (state, action) => {
      if (state.selectedOption !== action.payload) {
        state.selectedOption = action.payload;
      }
    },
  },
});

export const { selectOption } = radioSlice.actions;
export default radioSlice.reducer;
