// src/services/experiments.ts

import { api } from "@/lib/api";
import { Experiment, ExperimentDetail } from "@/types/types";

export async function listExperiments(): Promise<Experiment[]> {
  const { data } = await api.get("/experiments");
  return data;
}

export async function getExperimentDetail(id: string): Promise<ExperimentDetail> {
  const { data } = await api.get(`/experiments/${id}`);
  return data;
}