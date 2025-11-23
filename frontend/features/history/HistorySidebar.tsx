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
import { Spinner } from "@/components/ui/spinner"


export default function HistorySidebar() {

  const [experiments, setExperiments] = useState<Experiment[]>([]);

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    listExperiments().then(setExperiments).catch(console.error).finally(() => setLoading(false));
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
                {loading ? (
                  <Spinner />
                ) : (
                  experiments.map((item) => (
                    <HistoryItem key={item.id} experiment={item} />
                  ))
                )}
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
