import PromptInput from "@/features/experiment/PromptInputAndConfig/PromptInput";
import ResultsContainer from "@/features/experiment/results/ResultsContainer";
export default function ExperimentPage() {
    return (
        <div>
            <PromptInput />
            <ResultsContainer />
        </div>
    );
}