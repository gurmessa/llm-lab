// Enums
export enum ExperimentStatus {
  PENDING = "pending",
  RUNNING = "running",
  COMPLETED = "completed",
  FAILED = "failed",
  PARTIAL = "partial",
}

export enum ResponseStatus {
  PENDING = "pending",
  RUNNING = "running",
  COMPLETED = "completed",
  FAILED = "failed",
  PARTIAL = "partial",
}

// Response Record
export interface ResponseRecord {
  id: number;
  generated_text?: string;
  status: ResponseStatus;
  error_message?: string;
  latency_ms?: number;
  total_words?: number;
  total_sentences?: number;
  metrics?: Record<string, any>;
}

// Experiment Run
export interface ExperimentRun {
  id: number;
  temperature: number;
  top_p: number;
  max_output_tokens: number;
  created_at: string; // ISO datetime string
  response?: ResponseRecord;
}

// Experiment Run Create (input for creation)
export interface ExperimentRunCreate {
  temperature: number; // 0 - 2
  top_p: number;       // 0 - 1
  max_output_tokens: number;
}

// Experiment List
export interface Experiment {
  id: number;
  name?: string;
  total_runs: number;
  status: ExperimentStatus;
  created_at: string; // ISO datetime string
}

// Experiment Create (input for creation)
export interface ExperimentCreate {
  user_prompt: string;
  name?: string;
  model_name: string;
  total_runs: number;
  runs: ExperimentRunCreate[];
}

// Experiment Detail
export interface ExperimentDetail {
  id: number;
  name?: string;
  total_runs: number;
  status: ExperimentStatus;
  user_prompt: string;
  model_name: string;
  created_at: string; // ISO datetime string
  updated_at: string; // ISO datetime string
  runs: ExperimentRun[];
}
