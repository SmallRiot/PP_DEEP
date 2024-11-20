// src/features/fileSlice.js
import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";

// Асинхронное действие для загрузки файла на сервер
export const uploadFile = createAsyncThunk(
  "file/uploadFile",
  async (file, { rejectWithValue }) => {
    const formData = new FormData();
    formData.append("file", file);
    formData.forEach((value, key) => {
      console.log(`${key}: ${value}`);
    });

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/documents/",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
          // withCredentials: true,
        }
      );

      if (!response.ok) {
        console.log(response);
        throw new Error(response.json().toString());
      }

      return response.data; // Возвращаем данные сервера (например, URL файла)
    } catch (error) {
      return rejectWithValue(error.message); // Обрабатываем ошибки
    }
  }
);

const fileSlice = createSlice({
  name: "file",
  initialState: {
    uploadStatus: "idle", // 'idle' | 'loading' | 'succeeded' | 'failed'
    error: null,
  },
  reducers: {
    initFile: (state, action) => {
      state.uploadStatus = "idle";
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(uploadFile.pending, (state) => {
        state.uploadStatus = "loading";
        state.error = null;
      })
      .addCase(uploadFile.fulfilled, (state) => {
        state.uploadStatus = "succeeded";
      })
      .addCase(uploadFile.rejected, (state, action) => {
        state.uploadStatus = "failed";
        state.error = action.payload; // Сохраняем сообщение об ошибке
      });
  },
});

export default fileSlice.reducer;
export const { initFile } = fileSlice.actions;
