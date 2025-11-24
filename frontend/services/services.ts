// src/services/experiments.ts

import { api } from "@/lib/api";
import { Experiment, ExperimentDetail, ExperimentCreate } from "@/types/types";

export async function listExperiments(): Promise<Experiment[]> {
  const { data } = await api.get("/experiments/");
  return data;
}

export async function getExperimentDetail(id: string): Promise<ExperimentDetail> {
  const { data } = await api.get(`/experiments/${id}/`);
  return data;
}

export async function createExperiment(experiment: ExperimentCreate): Promise<ExperimentDetail> {
  const { data } = await api.post("/experiments/", experiment);
  return data;
}


export const exportExperimentCsv = async (experimentId: number) => {
  const response = await api.get(
    `/experiments/${experimentId}/export/csv/`,
    {
      responseType: "blob", // important for file downloads
    }
  );

  // Create a temp URL
  const url = window.URL.createObjectURL(new Blob([response.data]));

  // Create a download link
  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", `experiment_${experimentId}.csv`);
  document.body.appendChild(link);
  link.click();

  // Cleanup
  link.remove();
  window.URL.revokeObjectURL(url);
};
