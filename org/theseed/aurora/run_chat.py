#!/usr/bin/env python3

import os
import sys
from transformers import LlamaForCausalLM, AutoTokenizer
import torch

def load_model(model_path):
    """Load the model and tokenizer from the specified path."""
    print(f"Loading model from {model_path}...")

    # Check if we're dealing with a checkpoint directory
    if os.path.basename(model_path).startswith('checkpoint-'):
        checkpoint_path = model_path
    else:
        # Look for checkpoint directory
        checkpoint_dirs = [d for d in os.listdir(model_path) if d.startswith('checkpoint-')]
        if not checkpoint_dirs:
            raise ValueError(f"No checkpoint directory found in {model_path}")
        checkpoint_path = os.path.join(model_path, checkpoint_dirs[0])

    print(f"Using checkpoint: {checkpoint_path}")

    # Load tokenizer from the base model
    tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")

    # Load the fine-tuned model
    model = LlamaForCausalLM.from_pretrained(
        checkpoint_path,
        torch_dtype=torch.float16,
        device_map="auto"
    )

    return model, tokenizer

def generate_response(model, tokenizer, prompt, max_length=100):
    """Generate a response from the model."""
    # Format the prompt for chat
    formatted_prompt = f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"

    # Tokenize with attention mask
    inputs = tokenizer(
        formatted_prompt,
        return_tensors="pt",
        padding=True,
        truncation=True,
        return_attention_mask=True
    ).to(model.device)

    outputs = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_length=max_length,
        num_return_sequences=1,
        temperature=0.7,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Extract just the assistant's response
    response = response.split("<|im_start|>assistant\n")[-1].split("<|im_end|>")[0].strip()
    return response

def main():
    if len(sys.argv) != 2:
        print("Usage: python chat.py <path_to_model>")
        sys.exit(1)

    model_path = sys.argv[1]

    try:
        model, tokenizer = load_model(model_path)
        print("\nChat initialized! Type 'quit' to exit.")
        print("=" * 50)

        while True:
            user_input = input("\nYou: ").strip()
            if user_input.lower() == 'quit':
                break

            response = generate_response(model, tokenizer, user_input)
            print(f"\nModel: {response}")

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
