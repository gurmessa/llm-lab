"use client";

import { cn } from "@/lib/utils";

interface MetricProgressProps {
  label: string;
  value: number;
}

export const MetricProgress = ({ label, value }: MetricProgressProps) => {
  const getColorClass = (val: number) => {
    if (val >= 80) return "bg-green-500";
    if (val >= 50) return "bg-yellow-500";
    return "bg-red-500";
  };

  return (
    <div className="space-y-2">
      {/* Label and value */}
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-foreground">{label}</span>
        <span className="text-sm font-semibold text-foreground">{value}%</span>
      </div>

      {/* Progress bar */}
      <div className="h-2 w-full overflow-hidden rounded-full bg-muted">
        <div
          className={cn(
            "h-full transition-all duration-500",
            getColorClass(value)
          )}
          style={{ width: `${value}%` }}
        />
      </div>
    </div>
  );
};
