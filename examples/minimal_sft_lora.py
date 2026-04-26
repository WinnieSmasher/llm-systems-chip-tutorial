"""Minimal SFT + LoRA skeleton.

This is a teaching example. Real training needs cleaned data, eval sets,
checkpointing, and hardware-specific configuration.
"""

from datasets import load_dataset
from peft import LoraConfig
from trl import SFTConfig, SFTTrainer


MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"
DATASET_ID = "trl-lib/Capybara"


def main() -> None:
    dataset = load_dataset(DATASET_ID, split="train")

    peft_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    )

    args = SFTConfig(
        output_dir="outputs/qwen-lora-sft",
        per_device_train_batch_size=2,
        gradient_accumulation_steps=8,
        learning_rate=2e-5,
        num_train_epochs=1,
        max_length=2048,
        packing=True,
    )

    trainer = SFTTrainer(
        model=MODEL_ID,
        args=args,
        train_dataset=dataset,
        peft_config=peft_config,
    )
    trainer.train()
    trainer.save_model("outputs/qwen-lora-sft/final")


if __name__ == "__main__":
    main()

