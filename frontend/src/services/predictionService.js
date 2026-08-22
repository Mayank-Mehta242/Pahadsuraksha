import { api, USE_MOCK } from "./api.js";
import { mockPredictionResult } from "../data/mockData.js";

export const predictionService = {
  async predict(inputs) {
    if (USE_MOCK) {
      await new Promise((r) => setTimeout(r, 900));
      return mockPredictionResult;
    }
    const { data } = await api.post("/predict", inputs);
    return data;
  },
};
