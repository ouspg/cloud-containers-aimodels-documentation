import os
import torch
import yaml
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load config
with open("config.yaml", "r") as f:
    cfg = yaml.safe_load(f)

project_id = cfg["project_id"]
scratch_dir = cfg["scratch_dir"]

# Base model & checkpoint paths
base_model_id = cfg["base_model_id"]
merge_checkpoint = os.path.join(scratch_dir, cfg["merge_checkpoint"])
merged_output_dir = os.path.join(scratch_dir, cfg["merged_output_dir"])

# Load tokenizer & base model
tokenizer = AutoTokenizer.from_pretrained(base_model_id)
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_id,
    torch_dtype=torch.float16,
    load_in_8bit=False,
    trust_remote_code=True
)

# Load LoRA adapter and merge
model = PeftModel.from_pretrained(base_model, merge_checkpoint, from_transformers=True)
model = model.merge_and_unload()

# Save merged model
model.save_pretrained(merged_output_dir)
tokenizer.save_pretrained(merged_output_dir, safe_serialization=True)

print(f"Merge and save complete. Model saved to: {merged_output_dir}")
