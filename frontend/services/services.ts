// src/services/experiments.ts

import { api } from "@/lib/api";
import { Experiment } from "@/types/types";

export async function listExperiments(): Promise<Experiment[]> {
  const { data } = await api.get("/experiments");
  return data;
}
