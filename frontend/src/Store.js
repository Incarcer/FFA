import { configureStore } from '@reduxjs/toolkit';
import draftReducer from './slices/draftslice';
import recommendationReducer from './slices/recommendationslice';

export const store = configureStore({
  reducer: {
    draft: draftReducer,
    recommendations: recommendationReducer,
  },
});
