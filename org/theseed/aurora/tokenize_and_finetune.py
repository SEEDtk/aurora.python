#!/usr/bin/env python3
import sys
import os
from transformers import AutoTokenizer, LlamaForCausalLM, Trainer, TrainingArguments, TextDataset, DataCollatorForLanguageModeling
import torch

# Parse arguments
file_path = None
finetune = False
device = "auto"

args = sys.argv[1:]
if not args or len(args) > 3:
    print(f"Usage: python {sys.argv[0]} <path_to_plaintext_file> [--finetune] [--device=DEVICE]")
    sys.exit(1)

for arg in args:
    if arg == "--finetune":
        finetune = True
        print("Fine-tuning mode enabled.")
    elif arg.startswith("--device"):
        parts = arg.split("=")
        if len(parts) == 2:
            device = parts[1]
        else:
            idx = args.index(arg)
            if idx + 1 < len(args):
                device = args[idx + 1]
    elif not arg.startswith("--"):
        file_path = arg

if file_path is None:
    print(f"Usage: python {sys.argv[0]} <path_to_plaintext_file> [--finetune] [--device=DEVICE]")
    sys.exit(1)

# Device selection
def resolve_device(device):
    if device == "auto":
        if torch.cuda.is_available():
            return "cuda"
        elif torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"
    print(f"Using device: {device}")
    return device

selected_device = resolve_device(device)

# Load tokenizer
print("Loading tokenizer")
tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-step-50K-105b")
print(f"Tokenizer {tokenizer.name_or_path} loaded.")
# Read file
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()
print(f"Read {len(text)} characters from {file_path}.")
# Tokenize and count tokens
tokens = tokenizer(text, return_tensors=None)["input_ids"]
print(f"Total tokens: {len(tokens)}")

if finetune:
    model = LlamaForCausalLM.from_pretrained("keeeeenw/MicroLlama")
    model.to(selected_device)
    dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=file_path,
        block_size=128
    )
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )
    basename = os.path.splitext(os.path.basename(file_path))[0]
    output_dir = f"./finetuned-microllama-{basename}"
    training_args = TrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=True,
        num_train_epochs=1,
        per_device_train_batch_size=2,  # adjust if OOM
        save_steps=500,
        save_total_limit=2,
        fp16=True,  # :white_check_mark: mixed precision training (fast, lower memory)
        logging_steps=50,
        report_to="none",
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=dataset,
    )
    trainer.train()