import { api, USE_MOCK } from "./api.js";
import { mockReports } from "../data/mockData.js";

export const incidentService = {
  async list(status) {
    if (USE_MOCK) {
      await new Promise((r) => setTimeout(r, 400));
      return status ? mockReports.filter((report) => report.status === status) : mockReports;
    }
    const { data } = await api.get("/incidents", { params: status ? { status } : undefined });
    return data;
  },

  async listForAdmin() {
    if (USE_MOCK) return mockReports;
    const { data } = await api.get("/admin/incidents");
    return data;
  },

  async submit(formData) {
    if (USE_MOCK) {
      await new Promise((r) => setTimeout(r, 700));
      return { id: `r${Date.now()}`, status: "pending" };
    }
    const { data } = await api.post("/incidents", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return data;
  },

  async approve(id, comment = "") {
    if (USE_MOCK) return { id, status: "approved", reviewComment: comment };
    const { data } = await api.patch(`/incidents/${id}/approve`, { comment });
    return data;
  },

  async reject(id, comment = "") {
    if (USE_MOCK) return { id, status: "rejected", reviewComment: comment };
    const { data } = await api.patch(`/incidents/${id}/reject`, { comment });
    return data;
  },

  async update(id, fields) {
    if (USE_MOCK) return { id, ...fields, status: "pending", reviewComment: null };
    const { data } = await api.patch(`/incidents/${id}`, fields);
    return data;
  },

  async exportFile(format) {
    const response = await api.get(`/admin/export.${format}`, { responseType: "blob" });
    const url = URL.createObjectURL(response.data);
    const link = document.createElement("a");
    link.href = url;
    link.download = `pahadsuraksha_incidents.${format}`;
    link.click();
    URL.revokeObjectURL(url);
  },

  async delete(id) {
    if (USE_MOCK) return { id };
    const { data } = await api.delete(`/incidents/${id}`);
    return data;
  },
};
