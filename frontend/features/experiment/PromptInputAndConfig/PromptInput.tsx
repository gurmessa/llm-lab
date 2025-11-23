"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import { ChevronDown, ChevronUp } from "lucide-react";
import { RunConfig } from "./RunConfig";
import { toast } from "sonner";
import { useRouter } from "next/navigation";
import { createExperiment } from "@/services/services";
import { ExperimentDetail } from "@/types/types";

interface RunSettings {
  temp: number;
  topP: number;
}
interface PromptInputProps {
    experiment? : ExperimentDetail; 
}

export default function PromptInput({ experiment }: PromptInputProps) {
  const [prompt, setPrompt] = useState(experiment ? experiment.user_prompt : "");
  const [numberOfRuns, setNumberOfRuns] = useState(experiment ? experiment.total_runs : 2);
  const [runs, setRuns] = useState<RunSettings[]>(
    experiment
      ? experiment.runs.map((run) => ({
          temp: run.temperature,
          topP: run.top_p,
        }))
      :
    [
    { temp: 1, topP: 1 },
    { temp: 1, topP: 1 },
  ]);
  const [llmModel, setLlmModel] = useState(experiment ? experiment.model_name : "gpt-4.1-nano");
  const [maxTokens, setMaxTokens] = useState(experiment && experiment.runs.length > 0 ? experiment.runs[0].max_output_tokens : 200);
  const [isAdvancedOpen, setIsAdvancedOpen] = useState(false);

  const router = useRouter();

  const handleNumberOfRunsChange = (value: string) => {
    const num = parseInt(value) || 1;
    setNumberOfRuns(num);

    const newRuns = [...runs];
    while (newRuns.length < num) newRuns.push({ temp: 1, topP: 1 });
    while (newRuns.length > num) newRuns.pop();
    setRuns(newRuns);
  };

  const updateRunConfig = (
    index: number,
    field: "temp" | "topP",
    value: number
  ) => {
    const newRuns = [...runs];
    newRuns[index] = { ...newRuns[index], [field]: value };
    setRuns(newRuns);
  };

  const handleAutoFill = () => {
    const newRuns = runs.map(() => ({
      temp: Number((Math.random() * 2).toFixed(2)),
      topP: Number(Math.random().toFixed(2)),
    }));
    setRuns(newRuns);
  };

  const handleCreateExperiment = async () => {
    try {
      const experiment = {
        user_prompt: prompt,
        model_name: llmModel,
        total_runs: numberOfRuns,
        runs: runs.map((run) => ({
          temperature: run.temp,
          top_p: run.topP,
          max_output_tokens: maxTokens || 20,
        })),
      };
      const result = await createExperiment(experiment);
      toast.success("Experiment runned successfully!");
      router.push(`/${result.id}`);
    } catch (error) {
      toast.error("Failed to run experiment.");
    }
  }


  return (
    <div className="bg-background p-4 sm:p-8">
      <div className="max-w-4xl mx-auto space-y-8">
        <h1 className="text-3xl sm:text-4xl font-bold text-foreground">
          Experiment
        </h1>

        {/* Prompt */}
        <div className="space-y-2">
          <Label htmlFor="prompt" className="text-base font-medium">
            Prompt
          </Label>
          <Textarea
            id="prompt"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            className="min-h-[120px] resize-none rounded-2xl border-2 border-border"
            placeholder="Enter your prompt here..."
          />
        </div>

        {/* Number of Runs + Auto-fill */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:gap-4 gap-2">
          <div className="flex items-center gap-2">
            <Label htmlFor="runs" className="text-base font-medium whitespace-nowrap">
              Number of runs
            </Label>
            <Input
              id="runs"
              type="number"
              value={numberOfRuns}
              onChange={(e) => handleNumberOfRunsChange(e.target.value)}
              className="w-20 text-center"
              min={1}
              max={10}
            />
          </div>
          <Button
            onClick={handleAutoFill}
            variant="secondary"
          >
            Auto-fill Random Parameters
          </Button>
        </div>

        {/* Runs Config */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {runs.map((run, index) => (
            <RunConfig
              key={index}
              runNumber={index + 1}
              temp={run.temp}
              topP={run.topP}
              onTempChange={(value) => updateRunConfig(index, "temp", value)}
              onTopPChange={(value) => updateRunConfig(index, "topP", value)}
            />
          ))}
        </div>

        {/* Advanced Settings */}
        <Collapsible open={isAdvancedOpen} onOpenChange={setIsAdvancedOpen}>
          <CollapsibleTrigger className="flex items-center gap-2 text-base font-medium hover:text-foreground/80">
            {isAdvancedOpen ? <ChevronUp className="h-5 w-5" /> : <ChevronDown className="h-5 w-5" />}
            Advanced Settings
          </CollapsibleTrigger>
          <CollapsibleContent className="mt-4 space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center sm:gap-4 gap-2">
              <Label htmlFor="model" className="text-base font-medium whitespace-nowrap">
                LLM Model
              </Label>
              <Select value={llmModel} onValueChange={setLlmModel}>
                <SelectTrigger className="w-full sm:w-[180px]">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="gpt-4.1-nano">gpt-4.1-nano</SelectItem>
                  <SelectItem value="gpt-4.1-mini">gpt-4.1-mini</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="flex flex-col sm:flex-row sm:items-center sm:gap-4 gap-2">
              <Label htmlFor="tokens" className="text-base font-medium whitespace-nowrap">
                Max Tokens
              </Label>
              <Input
                id="tokens"
                type="number"
                value={maxTokens}
                onChange={(e) => setMaxTokens(Number(e.target.value))}
                className="w-full sm:w-[180px]"
                min={1}
              />
            </div>
          </CollapsibleContent>
        </Collapsible>

        {/* Run & Export Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 pt-4">
          <Button onClick={handleCreateExperiment} className="">
            Run Experiments
          </Button>
          <Button className="border-2 font-medium px-8 py-3 w-full sm:w-auto" variant="outline" disabled>
            Export CSV
          </Button>
        </div>
      </div>
    </div>
  );
}
