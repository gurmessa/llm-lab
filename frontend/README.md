# LLM Lab Frontend

## Project Overview

LLM Lab Frontend is a Next.js-based web application designed for experimenting with Large Language Model (LLM) parameters and visualizing results. The application allows users to create experiments with different temperature and top-p settings, run multiple iterations, and analyze the generated outputs through comprehensive metrics and visualizations.

## Tech Stack

- **Framework**: [Next.js 16.0.3](https://nextjs.org/)
- **Language**: [TypeScript](https://www.typescriptlang.org/)
- **Styling**: [Tailwind CSS v4](https://tailwindcss.com/)
- **UI Components**: [Shadcn](https://ui.shadcn.com/)
- **HTTP Client**: [Axios](https://axios-http.com/)
- **Icons**: [Lucide React](https://lucide.dev/)

## Folder Structure

```
frontend/
├── app/                    # Next.js app directory
│   ├── [id]/              # Dynamic route for experiment details
│   ├── components/        # Root-level components
│   └── layout.tsx         # Root layout
|   └── page.tsx           # New Experiment Page
├── components/            # Shared components
│   ├── layout/            # Layout components (Header, Footer)
│   └── ui/                # Shadcn UI components
├── features/              # Feature-based organization
│   ├── experiment/        # Experiment-related components
│   └── history/           # History sidebar components
├── lib/                   # Utility libraries and configurations
├── public/                # Static assets
├── services/              # API Services
├── types/                 # TypeScript type definitions
└── utils/                 # Utility functions
```

## Setup Instructions

### Prerequisites

- [Node.js](https://nodejs.org/) (version 18 or higher)
- npm (comes with Node.js) or yarn

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

### Environment Variables

Create a `.env` file in the frontend directory with the following variable:

```env
NEXT_PUBLIC_API_URL=http://localhost:8083/api/v1
```

Adjust the API URL according to your backend configuration.

### Development Server

Start the development server:

```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

### Build for Production

```bash
npm run build
# or
yarn build
```

### Linting

```bash
npm run lint
# or
yarn lint
```

## Architecture Documentation

### Component Structure

The application follows a feature-based component organization:

- **app/**: Contains page components and the root layout
- **components/**: Shared UI components used across features
- **features/**: Feature-specific components organized by domain
- **ui/**: Reusable UI primitives with Shadcn and Tailwind CSS

### Feature Organization

1. **Experiment Feature** (`features/experiment/`)
   - Prompt input and configuration
   - Results display and visualization
   - Run parameter controls

2. **History Feature** (`features/history/`)
   - Experiment history sidebar
   - Previous experiment navigation

### API Service Layer

The application uses a service layer (`services/services.ts`) that abstracts API calls using Axios. This layer handles:
- Experiment creation
- Experiment retrieval
- Experiments List
- CSV export functionality

### Type Definitions

All data structures are strongly typed using TypeScript interfaces and enums defined in `types/types.ts`:
- Experiment and ExperimentRun interfaces
- ResponseRecord for API responses
- Status enums for experiment and response states


## Quick Start Guide

### 1. Create a New Experiment

1. Navigate to the home page (`/`)
2. Enter your prompt in the text area
3. Configure the number of runs (1-10)
4. Set parameters for each run:
   - Temperature (0-2)
   - Top-p (0-1)
   - Max tokens (0-2000)

### 2. Auto-fill Parameters

Use the "Auto-fill Random Parameters" button to generate random temperature and top-p values for all runs.

### 3. Advanced Settings

Expand the "Advanced Settings" section to configure:
- LLM Model (gpt-4.1-nano or gpt-4.1-mini)
- Max Tokens for output

### 4. Run Experiments

Click "Run Experiments" to execute your configured experiment. The application will:
1. Send the experiment configuration to the backend
2. Display real-time progress
3. Show results when complete

### 5. View Results

After completion, the application displays:
- Generated text outputs
- Performance metrics (coherence, relevance, structure, etc.)
- Visual charts comparing runs
- Word and sentence count statistics

### 6. Export Data

Click "Export CSV" to download experiment results as a CSV file.

### 7. View History

Use the sidebar to navigate between previous experiments.

## Key Features

### Experiment Creation
- Configurable prompt input
- Multiple run configuration
- Parameter customization (temperature, top-p)
- Model selection
- Output token limits

### Results Visualization
- Side-by-side output comparison
- Performance metrics dashboard
- Interactive charts (Recharts)
- Word and sentence statistics

### History Tracking
- Persistent experiment history
- Quick navigation between experiments
- Status indicators (pending, running, completed, failed)

### Data Export
- CSV export functionality
- Complete experiment data download

### Responsive Design
- Mobile-friendly interface
- Collapsible sidebar
- Adaptive layouts for different screen sizes
