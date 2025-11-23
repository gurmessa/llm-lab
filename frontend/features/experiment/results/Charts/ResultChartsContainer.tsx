"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"
import { BarChart, Bar, XAxis, CartesianGrid } from "recharts"
import {ExperimentDetail} from "@/types/types"
import { MetricsChart } from "./components/MetricsChart"
import { WordsAndSentencesChart } from "./components/WordsAndSentencesChart"

interface ResultChartsContainerProps {
  experiment: ExperimentDetail
}

export function ResultChartsContainer({ experiment }: ResultChartsContainerProps) {

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4  p-6 md:p-8 lg:p-12">
      
      {/* Metrics Chart */}
        <MetricsChart experiment={experiment} />
      {/* Words & Sentences Chart */}
        <WordsAndSentencesChart experiment={experiment} />
    </div>
  )
}
