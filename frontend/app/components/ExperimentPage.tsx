import PromptInput from "@/features/experiment/PromptInputAndConfig/PromptInput";
import ResultsContainer from "@/features/experiment/results/ResultsContainer";
import {ExperimentDetail} from "@/types/types";


interface ExperimentPageProps {
  experiment?: ExperimentDetail;
}
export default function ExperimentPage({ experiment }: ExperimentPageProps) {

    return (
        <div>
            <PromptInput />
            <ResultsContainer experiment={experiment} />
        </div>
    );
}