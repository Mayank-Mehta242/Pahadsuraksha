import { api, USE_MOCK } from "./api.js";
import { mockWeather } from "../data/mockData.js";

export const weatherService = {
  async getWeather(lat, lng) {
    if (USE_MOCK) {
      await new Promise((r) => setTimeout(r, 500));
      return mockWeather;
    }
    const { data } = await api.get("/weather", { params: { lat, lng } });
    return data;
  },
};
