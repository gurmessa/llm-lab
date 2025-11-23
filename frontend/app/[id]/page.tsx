import { ExperimentDetail as Experiment } from "@/types/types";
import { getExperimentDetail } from '@/services/services';
import ExperimentPage from "../components/ExperimentPage";

interface PageProps {
  params: { id: string };
}

export async function generateMetadata({ params }: PageProps) {
  const { id } =  await params;
  const experiment: Experiment = await getExperimentDetail(id);

  return {
    title: experiment.name || `Experiment ${params.id}`,
    description: experiment.user_prompt,
    openGraph: {
      title: experiment.name || `Experiment ${params.id}`,
      description: experiment.user_prompt,
    },
  };
}

export default async function ExperimentDetail({ params }: PageProps) {
  const { id } =  await params;
  const experiment: Experiment = await getExperimentDetail(id);

  return (
    <ExperimentPage experiment={experiment} />
  );

}
