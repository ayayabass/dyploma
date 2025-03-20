import torch
from transformers import LlamaForCausalLM, LlamaTokenizer, TrainingArguments, Trainer
from datasets import load_dataset, DatasetDict
import evaluate
import bitsandbytes as bnb
from peft import LoraConfig, get_peft_model, TaskType

tokenizer = LlamaTokenizer.from_pretrained("meta-llama/Llama-3.2-3B-Instruct")
model = LlamaForCausalLM.from_pretrained("meta-llama/Llama-3.2-3B-Instruct", load_in_8bit=True, device_map="auto")

config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=8,
    lora_alpha=32,
    lora_dropout=0.1,
    target_modules=["q_proj", "v_proj"]
)
model = get_peft_model(model, config)

dataset = load_dataset("ja_ua_dataset")
def preprocess_function(sentences):
    inputs = [f"Translate Japanese to Ukrainian: {text}" for text in sentences["japanese"]]
    model_inputs = tokenizer(inputs, max_length=512, truncation=True)
    labels = tokenizer(sentences["ukrainian"], max_length=512, truncation=True)
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

tokenized_datasets = dataset.map(preprocess_function, batched=True)

chrf = evaluate.load("chrf")
bertscore = evaluate.load("bertscore")

def compute_metrics(eval_pred):
    preds, labels = eval_pred
    decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)
    
    chrf_score = chrf.compute(predictions=decoded_preds, references=decoded_labels)
    bertscore_score = bertscore.compute(predictions=decoded_preds, references=decoded_labels, lang="uk")
    
    return {"chrF": chrf_score["score"], "BERTScore": sum(bertscore_score["f1"]) / len(bertscore_score["f1"])}

training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    num_train_epochs=10,
    weight_decay=0.01,
    save_total_limit=2,
    fp16=True,
    push_to_hub=False
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

trainer.train()

trainer.save_model("./ja_ua_fine_tuned_llama")