import { createSlice } from "@reduxjs/toolkit";

const docsSlice = createSlice({
  name: "docs",
  initialState: {
    routes: [],
  },
  reducers: {
    setRouts: (state, action) => {
      state.routes = action.payload;
    },
  },
});

export const getPathIndexByName = (state, pathName) =>
  state.routes.findIndex((el) => el.initPath === pathName);

export const { setRouts } = docsSlice.actions;
export default docsSlice.reducer;
