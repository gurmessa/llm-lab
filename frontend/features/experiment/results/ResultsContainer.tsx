import { ResultList } from "./ResultList";
import {ResultChartsContainer} from "./Charts/ResultChartsContainer";
import { ExperimentDetail, ResponseStatus, ExperimentStatus } from "@/types/types";

const mockExperiment: ExperimentDetail = {
  id: 1,
  name: "Text Generation Quality Assessment",
  total_runs: 2,
  status: ExperimentStatus.COMPLETED,
  user_prompt: "Generate a description about Lorem Ipsum",
  model_name: "gpt-4",
  created_at: new Date().toISOString(),
  updated_at: new Date().toISOString(),
  runs: [
    {
      id: 1,
      temperature: 1,
      top_p: 1,
      max_output_tokens: 50,
      created_at: new Date().toISOString(),
      response: {
        id: 1,
        generated_text:
          "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type book",
        status: ResponseStatus.COMPLETED,
        latency_ms: 1250,
        total_words: 1,
        total_sentences: 1,
        metrics: {
          overall_score: 98,
          completeness: 80,
          coherence: 80,
          relevance: 30,
          structure: 60,
        },
      },
    },
    {
      id: 2,
      temperature: 1,
      top_p: 1,
      max_output_tokens: 50,
      created_at: new Date().toISOString(),
      response: {
        id: 2,
        generated_text:
          "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type book",
        status: ResponseStatus.COMPLETED,
        latency_ms: 1180,
        total_words: 1,
        total_sentences: 1,
        metrics: {
          overall_score: 70,
          completeness: 10,
          coherence: 80,
          relevance: 30,
          structure: 60,
        },
      },
    },
  ],
};

interface ResultsContainerProps {
  experiment? : ExperimentDetail;
}
const ResultsContainer = ({ experiment }: ResultsContainerProps) => {
  if (!experiment) {
    return null;
  }
  
  return (
    <>
      <ResultList experiment={experiment} />
      <ResultChartsContainer experiment={experiment} />
    </>
  );
};

export default ResultsContainer;
