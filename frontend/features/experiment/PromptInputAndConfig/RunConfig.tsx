"use client";

import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";
import { Input } from "@/components/ui/input";

interface RunConfigProps {
  runNumber: number;
  temp: number;
  topP: number;
  onTempChange: (value: number) => void;
  onTopPChange: (value: number) => void;
}

export const RunConfig = ({
  runNumber,
  temp,
  topP,
  onTempChange,
  onTopPChange,
}: RunConfigProps) => {
  return (
    <div className="rounded-2xl bg-gray-200 p-4 sm:p-6 space-y-4 sm:space-y-6">
      <h3 className="text-sm sm:text-base font-medium text-foreground mb-0">
        Run {runNumber}
      </h3>

      {/* Temperature */}
      <div className="">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 sm:gap-0">
          <Label className="text-sm text-muted-foreground">Temp</Label>
          <Input
            type="number"
            value={temp}
            onChange={(e) => onTempChange(parseFloat(e.target.value) || 0)}
            className="w-full sm:w-24 h-8 text-center text-sm"
            min={0}
            max={2}
            step={0.1}
          />
        </div>
        <Slider
          value={[temp]}
          onValueChange={(values) => onTempChange(values[0])}
          min={0}
          max={2}
          step={0.1}
          className="w-full"
        />
      </div>

      {/* Top P */}
      <div className="">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 sm:gap-0">
          <Label className="text-sm text-muted-foreground">Top P</Label>
          <Input
            type="number"
            value={topP}
            onChange={(e) => onTopPChange(parseFloat(e.target.value) || 0)}
            className="w-full sm:w-24 h-8 text-center text-sm"
            min={0}
            max={1}
            step={0.1}
          />
        </div>
        <Slider
          value={[topP]}
          onValueChange={(values) => onTopPChange(values[0])}
          min={0}
          max={1}
          step={0.1}
          className="w-full"
        />
      </div>
    </div>
  );
};
