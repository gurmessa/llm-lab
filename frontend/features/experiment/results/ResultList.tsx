"use client"; // optional, needed if you use browser-only APIs or state

import { useMemo } from "react";
import { ResultItem } from "./ResultItem";
import { ExperimentDetail } from "@/types/types";

interface ResultDetailProps {
  experiment: ExperimentDetail;
}

export const ResultList = ({ experiment }: ResultDetailProps) => {
  // Memoize sorting for performance
  const rankedRuns = useMemo(() => {
    return [...experiment.runs].sort((a, b) => {
      const scoreA = a.response?.metrics?.overall_score || 0;
      const scoreB = b.response?.metrics?.overall_score || 0;
      return scoreB - scoreA;
    });
  }, [experiment.runs]);

  return (
    <div className="min-h-screen bg-background p-6 md:p-8 lg:p-12">
      <div className="mx-auto max-w-5xl space-y-8">
        {/* Header */}
        <div className="space-y-2">
          <h1 className="text-3xl font-bold tracking-tight text-foreground">
            Results ({experiment.total_runs} Total Runs)
          </h1>
          {experiment.name && (
            <p className="text-lg text-muted-foreground">{experiment.name}</p>
          )}
        </div>

        {/* Run Cards */}
        <div className="space-y-6">
          {rankedRuns.map((run, index) => (
            <ResultItem
              key={run.id}
              run={run}
              rank={index + 1}
              overallScore={run.response?.metrics?.overall_score || 0}
            />
          ))}
        </div>
      </div>
    </div>
  );
};
