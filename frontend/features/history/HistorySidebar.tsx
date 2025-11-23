"use client";
import { useEffect, useState } from "react";
import {
  Sidebar,
  SidebarContent,
  SidebarHeader,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupLabel,
  SidebarGroupContent,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
  useSidebar
} from "@/components/ui/sidebar";
import { PlusSquare } from "lucide-react";
import HistoryItem from "./HistoryItem";
import { Experiment, ExperimentStatus } from "@/types/types";
import { listExperiments } from "@/services/services";


export default function HistorySidebar() {
  /*const historyList: Experiment[] = [
    { id: 1, name: "Experiment 1 Long Name ", total_runs: 5, status: ExperimentStatus.COMPLETED, created_at: new Date().toISOString() },
    { id: 2, name: "Experiment 2", total_runs: 3, status: ExperimentStatus.RUNNING, created_at: new Date(Date.now() - 86400000).toISOString() }, // yesterday's date
    { id: 3, name: "Experiment 3", total_runs: 8, status: ExperimentStatus.FAILED, created_at: new Date().toISOString() },
    { id: 4, name: "Experiment 4", total_runs: 2, status: ExperimentStatus.PENDING, created_at: new Date().toISOString() },
    { id: 5, name: "Experiment 5", total_runs: 10, status: ExperimentStatus.PARTIAL, created_at: new Date().toISOString() },
  ];*/

  const [experiments, setExperiments] = useState<Experiment[]>([]);

  useEffect(() => {
    listExperiments().then(setExperiments).catch(console.error);
  }, []);


  const { state } = useSidebar();

  const isCollapsed = state === "collapsed";

  return (
    <Sidebar collapsible="icon" variant="sidebar">
      {!isCollapsed && (
      <SidebarHeader>
        <div className="p-4 font-bold">LLM Lab</div>
      </SidebarHeader>
      )}

      <SidebarContent>

        {/* Navigation */}
        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton asChild>
                  <a href="/">
                    <PlusSquare />
                    <span>New Experiment</span>
                  </a>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>


        {/* History */}
        {!isCollapsed && 
          <SidebarGroup>
            <SidebarGroupLabel>History</SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu>
                {experiments.map((item) => (
                  <HistoryItem key={item.id} experiment={item} />
                ))}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        }

      </SidebarContent>

      {!isCollapsed && <SidebarFooter>
        <div className="p-4">LLM Lab © 2025</div>
      </SidebarFooter>
      }
    </Sidebar>
  );
}
