import { configureStore } from "@reduxjs/toolkit";
import radioReducer from "../redux/slices/radioSlice";
import docsReducer from "../redux/slices/docsSlice";
import fileReducer from "../redux/slices/fileSlice";

const store = configureStore({
  reducer: {
    radio: radioReducer,
    docs: docsReducer,
    file: fileReducer,
  },
});

export default store;
