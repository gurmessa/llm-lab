"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"
import { BarChart, Bar, XAxis, CartesianGrid } from "recharts"
import {ExperimentDetail} from "@/types/types"

interface WordsAndSentencesChartProps {
  experiment: ExperimentDetail
}

export function WordsAndSentencesChart({ experiment }: WordsAndSentencesChartProps) {
  // Prepare chart data
  const wordsSentencesData = experiment.runs.map((run, index) => ({
    run: `Run ${index + 1} (Temp: ${run.temperature}, Top P: ${run.top_p})`,
    words: run?.response?.total_words,
    sentences: run?.response?.total_sentences,
  }))

  return (
    <>
      <Card>
        <CardHeader>
          <CardTitle>Words & Sentences per Run</CardTitle>
        </CardHeader>
        <CardContent>
          <ChartContainer
            config={{
              words: { label: "Words", color: "var(--chart-1)" },
              sentences: { label: "Sentences", color: "var(--chart-2)" },
            }}
          >
            <BarChart accessibilityLayer data={wordsSentencesData}>
              <CartesianGrid vertical={false} />
              <XAxis dataKey="run" tickLine={false} axisLine={false} />
              <ChartTooltip cursor={false} content={<ChartTooltipContent indicator="dashed" />} />
              <Bar dataKey="words" fill="var(--chart-1)" radius={4} />
              <Bar dataKey="sentences" fill="var(--chart-2)" radius={4} />
            </BarChart>
          </ChartContainer>
        </CardContent>
      </Card>

    </>
  )
}
