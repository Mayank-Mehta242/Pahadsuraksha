import { api, USE_MOCK } from "./api.js";
import { mockDistricts, mockStats, mockHistorical } from "../data/mockData.js";

export const districtService = {
  async list() {
    if (USE_MOCK) {
      await new Promise((r) => setTimeout(r, 400));
      return mockDistricts;
    }
    const { data } = await api.get("/districts");
    return data;
  },

  async stats() {
    if (USE_MOCK) {
      await new Promise((r) => setTimeout(r, 300));
      return mockStats;
    }
    const { data } = await api.get("/districts/stats");
    return data;
  },

  async historical() {
    if (USE_MOCK) {
      await new Promise((r) => setTimeout(r, 400));
      return mockHistorical;
    }
    const { data } = await api.get("/districts/historical");
    return data;
  },
};
