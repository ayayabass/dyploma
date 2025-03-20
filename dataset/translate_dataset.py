from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-uk")
model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-uk")

#text = ""
#inputs = tokenizer.encode(text, return_tensors='pt')
#output = model.generate(inputs, max_new_tokens=200)

if __name__ == '__main__':
    en_file = open("eng.txt", 'r', encoding='utf-8')
    ua_file = open("ukr.txt", 'w', encoding='utf-8')
    for line in en_file:
        inputs = tokenizer.encode(line, return_tensors='pt')
        output = model.generate(inputs, max_new_tokens=400)
        translation = tokenizer.decode(output[0], skip_special_tokens=True)
        ua_file.write(translation)
        ua_file.write('\n')