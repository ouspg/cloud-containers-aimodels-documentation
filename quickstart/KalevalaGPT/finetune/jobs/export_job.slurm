#!/bin/bash
#SBATCH --job-name=tinyllama_export
#SBATCH --account=project_2014746
#SBATCH --ntasks=1
#SBATCH --nodes=1  
#SBATCH --cpus-per-task=4
#SBATCH --mem=16g
#SBATCH --time=01:00:00
#SBATCH --partition=gpu
#SBATCH --gres=gpu:v100:1

source ~/myenv/bin/activate

export HF_HOME=/scratch/project_2014746/huggingface
export TRANSFORMERS_CACHE=/scratch/project_2014746/transformers
export HF_DATASETS_CACHE=/scratch/project_2014746/datasets
export HF_METRICS_CACHE=/scratch/project_2014746/metrics

echo "export_job.slurm starting"

# Merge model
srun python -u ~/ai-trainer/merge_export_model.py

echo "converting the model to GGUF"
# Convert merged model to GGUF
srun python /scratch/project_2014746/llama.cpp/convert_hf_to_gguf.py \
    /scratch/project_2014746/tinyllama-kalevala-merged \
    --outfile /scratch/project_2014746/tinyllama-kalevala-chat.gguf

echo "export_job.slurm finished"