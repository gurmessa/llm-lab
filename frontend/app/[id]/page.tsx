import { ExperimentDetail as Experiment } from "@/types/types";
import { getExperimentDetail } from '@/services/services';
import ExperimentPage from "../components/ExperimentPage";

interface PageProps {
  params: { id: string };
}

export default async function ExperimentDetail({ params }: PageProps) {
  const { id } =  await params;
  const experiment: Experiment = await getExperimentDetail(id);

  return (
    <ExperimentPage experiment={experiment} />
  );

}
