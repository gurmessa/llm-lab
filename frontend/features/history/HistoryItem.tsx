import {
  SidebarMenuItem,
  SidebarMenuButton,
} from "@/components/ui/sidebar";
import { Badge } from "@/components/ui/badge"
import { Clock } from "lucide-react";
import { Experiment, ExperimentStatus } from "@/types/types";
import moment from "moment";
import Link from "next/link";

interface ExperimentItemProps {
  experiment: Experiment;
}

export default function HistoryItem({ experiment }: ExperimentItemProps) {

  const humanDate = moment(experiment.created_at).fromNow(); // e.g., "3 hours ago"
  const statusVariant = (() => {
    switch (experiment.status) {
      case ExperimentStatus.RUNNING:
        return "default";
      case ExperimentStatus.PENDING:
        return "secondary";
      case ExperimentStatus.COMPLETED:
        return "outline";
      case ExperimentStatus.FAILED:
        return "destructive";
      case ExperimentStatus.PARTIAL:
        return "default"; 
      default:
        return "default";
    }
  })();

  return (
    <SidebarMenuItem>
      <Link
        href={`/${experiment.id}`}
        className="flex flex-col gap-2 p-3 bg-background rounded-lg shadow-sm hover:shadow-md transition-shadow duration-150 hover:bg-accent/10"
      >
        {/* First row: Experiment name */}
        <div className="flex items-center space-x-2 w-full">
          <Clock className="w-4 h-4 text-muted-foreground" />
          <span className="font-medium truncate">{experiment.name ?? "Unnamed Experiment"}</span>
        </div>

        {/* Second row: Runs and status */}
        <div className="flex items-center justify-between text-sm text-muted-foreground gap-2 mt-1">
          <span>{experiment.total_runs} runs</span>
          <Badge variant={statusVariant}>{experiment.status}</Badge>
        </div>

        {/* Optional: time ago */}
        <div className="text-sm text-muted-foreground mt-1">
          {humanDate}
        </div>
      </Link>
    </SidebarMenuItem>
  );
}