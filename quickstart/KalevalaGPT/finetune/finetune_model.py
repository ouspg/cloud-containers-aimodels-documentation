import os
import yaml
from datasets import load_dataset, Dataset
from peft import LoraConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainingArguments
from trl import SFTTrainer

# === LOAD CONFIG ===
with open("config.yaml", "r") as f:
    cfg = yaml.safe_load(f)

# === CONFIGURATION ===
project_id = cfg["project_id"]
scratch_dir = f"/scratch/{project_id}"
train_dataset = cfg["train_dataset"]
eval_dataset = cfg["eval_dataset"]
base_model_id = cfg["base_model_id"]
output_model = os.path.join(scratch_dir, cfg["output_model_name"])

# Redirect Hugging Face cache and temporary files to scratch space
os.environ["HF_HOME"] = os.path.join(scratch_dir, "huggingface")
os.environ["TRANSFORMERS_CACHE"] = os.path.join(scratch_dir, "transformers")
os.environ["HF_DATASETS_CACHE"] = os.path.join(scratch_dir, "datasets")
os.environ["HF_METRICS_CACHE"] = os.path.join(scratch_dir, "metrics")

# Ensure cache directories exist
for path in [os.environ["HF_HOME"], os.environ["TRANSFORMERS_CACHE"], os.environ["HF_DATASETS_CACHE"], os.environ["HF_METRICS_CACHE"]]:
    os.makedirs(path, exist_ok=True)

# === DATA PREPARATION ===
def prepare_train_data(dataset_name, split):
    data = load_dataset(dataset_name, split=split)
    data_df = data.to_pandas()

    data_df["text"] = data_df.apply(
        lambda x: f"<|im_start|>user\n{x['prompt']}<|im_end|>\n<|im_start|>assistant\n{x['response']}<|im_end|>\n",
        axis=1
    )

    data_df = data_df[["text"]]
    return Dataset.from_pandas(data_df)

train_data = prepare_train_data(train_dataset, "train").shuffle(seed=42)

print(f"Data prepared: \ntrain_data: {train_data},\neval_data: {eval_dataset}")

# === MODEL & TOKENIZER ===
def get_model_and_tokenizer(model_id):
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    tokenizer.pad_token = tokenizer.eos_token

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype="float16",
        bnb_4bit_use_double_quant=True
    )

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map="auto"
    )

    model.config.use_cache = False
    model.config.pretraining_tp = 1
    return model, tokenizer

model, tokenizer = get_model_and_tokenizer(base_model_id)

# === LoRA CONFIG ===
peft_config = LoraConfig(
    r=cfg["lora_r"],
    lora_alpha=cfg["lora_alpha"],
    lora_dropout=cfg["lora_dropout"],
    bias=cfg["lora_bias"],
    task_type="CAUSAL_LM"
)

# === TRAINING ARGS ===
training_arguments = TrainingArguments(
    output_dir=output_model,
    per_device_train_batch_size=cfg["per_device_train_batch_size"],
    gradient_accumulation_steps=cfg["gradient_accumulation_steps"],
    optim=cfg["optim"],
    learning_rate=cfg["learning_rate"],
    lr_scheduler_type=cfg["lr_scheduler_type"],
    save_strategy=cfg["save_strategy"],
    eval_strategy=cfg["eval_strategy"],
    load_best_model_at_end=cfg["load_best_model_at_end"],
    metric_for_best_model=cfg["metric_for_best_model"],
    greater_is_better=cfg["greater_is_better"],
    logging_steps=cfg["logging_steps"],
    num_train_epochs=cfg["num_train_epochs"],
    fp16=cfg["fp16"],
    report_to=[],
    save_total_limit=cfg["save_total_limit"]
)

# === TRAINER ===
trainer = SFTTrainer(
    model=model,
    train_dataset=train_data,
    eval_dataset=eval_dataset,
    processing_class=tokenizer,
    peft_config=peft_config,
    args=training_arguments
)

# === TRAIN ===
trainer.train()

print(f"Fine-tuning complete. Model saved to: {output_model}")
