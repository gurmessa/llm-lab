"use client";

import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ExperimentRun } from "@/types/types";
import { MetricProgress } from "./MetricProgress";
import { cn } from "@/lib/utils";

interface ResultItemProps {
  run: ExperimentRun;
  rank: number;
}

export const ResultItem = ({
  run,
  rank,
}: ResultItemProps) => {
  const response = run.response;
  const metrics = response?.metrics || {};

  const availableMetricsKeys = Object.keys(metrics).filter((key) => metrics[key] !== undefined && key !== "overall");
  
  const metricsToPercentage = (value: any) => {
    const num = Number(value);
    if (isNaN(num)) return 0;
    return Math.ceil(num * 100);
  }
  const availableMetrics = availableMetricsKeys.map((key) => ({
    label: key.charAt(0).toUpperCase() + key.slice(1),
    value: metricsToPercentage(metrics[key]),
  }));


  return (
    <Card className="overflow-hidden border-2 border-border transition-shadow hover:shadow-lg">
      <div className="p-6 space-y-4">
        {/* Header with Rank and Score */}
        <div className="flex items-start justify-between gap-4">
        <Badge variant={"secondary"}>
          Rank #{rank}
        </Badge>

        <Badge>
          Overall Score: {metricsToPercentage(metrics?.overall)}%
        </Badge>
        </div>

        {/* Parameters */}
        <div className="flex flex-wrap items-center gap-6 text-sm text-muted-foreground">
          <Badge variant={"outline"}>Temp: {run.temperature}</Badge>
          <Badge variant={"outline"}>Top P: {run.top_p}</Badge>
        </div>

        {/* Generated Text */}
        {response?.generated_text && (
          <div className="rounded-lg bg-gray-100 p-4">
            <p className="text-sm leading-relaxed text-foreground/90">
              {response.generated_text}
            </p>
          </div>
        )}

        {/* Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-4 pt-2">
          {availableMetrics.map((metric) => (
            <MetricProgress
              key={metric.label}
              label={metric.label}
              value={metric.value}
            />
          ))}

        </div>

        {/* Footer Stats */}
        <div className="flex flex-wrap items-center gap-6 pt-2 text-sm text-muted-foreground">
          <div>
            <span className="font-medium">Words:</span> {response?.total_words || 1}
          </div>
          <div>
            <span className="font-medium">Sentences:</span> {response?.total_sentences || 1}
          </div>
          <div>
            <span className="font-medium">Max Token:</span> {run.max_output_tokens}
          </div>
        </div>
      </div>
    </Card>
  );
};
