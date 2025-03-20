import torch
from transformers import LlamaForCausalLM, LlamaTokenizer

model_path = "./ja_ua_fine_tuned_llama"
tokenizer = LlamaTokenizer.from_pretrained(model_path)
model = LlamaForCausalLM.from_pretrained(model_path, device_map="auto")

def translate(sentence, max_length=10000):
    prompt = f"Translate from Japanese into Ukrainian: {sentence}"
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

    with torch.no_grad():
        output = model.generate(**inputs, max_length=max_length, do_sample=False)

    return tokenizer.decode(output[0], skip_special_tokens=True)

ja_sentence = "白いうさぎ原っぱで跳ねる"
translation = translate(ja_sentence)
print("Ukrainian Translation:", translation)