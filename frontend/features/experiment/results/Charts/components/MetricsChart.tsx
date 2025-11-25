"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"
import { BarChart, Bar, XAxis, CartesianGrid } from "recharts"
import {ExperimentDetail} from "@/types/types"

interface MetricsChartProps {
  experiment: ExperimentDetail
}

export function MetricsChart({ experiment }: MetricsChartProps) {
  const toPct = (v?: number | null) => v != null ? Math.ceil(v * 100) : null;

const metricsData = experiment.runs.map((run, index) => ({
  run: `Run ${index + 1} (T: ${run.temperature}, P: ${run.top_p})`,
  overall: toPct(run?.response?.metrics?.overall),
  coherence: toPct(run?.response?.metrics?.coherence),
  relevance: toPct(run?.response?.metrics?.relevance),
  structure: toPct(run?.response?.metrics?.structure),
  lexical_diversity: toPct(run?.response?.metrics?.lexical_diversity),
}));

  const metricsConfig = {
    overall: { label: "Overall", color: "var(--chart-1)" },
    coherence: { label: "Coherence", color: "var(--chart-3)" },
    relevance: { label: "Relevance", color: "var(--chart-4)" },
    structure: { label: "Structure", color: "var(--chart-5)" },
    lexical_diversity: { label: "Lexical Diversity", color: "var(--chart-6)" },
  }

  return (
    <> 
      {/* Metrics Chart */}
      <Card>
        <CardHeader>
          <CardTitle>Metrics per Run</CardTitle>
        </CardHeader>
        <CardContent>
          <ChartContainer config={metricsConfig}>
            <BarChart accessibilityLayer data={metricsData}>
              <CartesianGrid vertical={false} />
              <XAxis dataKey="run" tickLine={false} axisLine={false} />
              <ChartTooltip cursor={false} content={<ChartTooltipContent indicator="dashed" />} />
              {Object.keys(metricsConfig).map((key) => (
                <Bar key={key} dataKey={key} fill={metricsConfig[key as keyof typeof metricsConfig].color} radius={4} />
              ))}
            </BarChart>
          </ChartContainer>
        </CardContent>
      </Card>
    </>
  )
}
