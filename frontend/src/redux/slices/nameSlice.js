import { createSlice } from "@reduxjs/toolkit";

const nameSlice = createSlice({
  name: "name",
  initialState: {
    check: {
      download: false,
      name: "",
    },
    statement: {
      download: false,
      name: "",
    },
  },
  reducers: {
    setCheck: (state, action) => {
      state.check = action.payload;
    },
    setStatement: (state, action) => {
      state.statement = action.payload;
    },
  },
});

export const { setCheck, setStatement } = nameSlice.actions;
export default nameSlice.reducer;
