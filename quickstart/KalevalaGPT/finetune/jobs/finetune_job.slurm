#!/bin/bash
#SBATCH --job-name=tinyllama_finetune
#SBATCH --account=project_2014746
#SBATCH --ntasks=1
#SBATCH --nodes=1  
#SBATCH --cpus-per-task=4
#SBATCH --mem=16g
#SBATCH --time=02:00:00
#SBATCH --partition=gpu
#SBATCH --gres=gpu:v100:1

source ~/myenv/bin/activate

export HF_HOME=/scratch/project_2014746/huggingface
export TRANSFORMERS_CACHE=/scratch/project_2014746/transformers
export HF_DATASETS_CACHE=/scratch/project_2014746/datasets
export HF_METRICS_CACHE=/scratch/project_2014746/metrics

echo "finetune_job.slurm starting"
srun python -u ~/ai-trainer/finetune_model.py
echo "finetune_job.slurm finished"