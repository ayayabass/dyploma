import json
import datasets

ja_files = ["aobun_ja.txt", "nipon_ja.txt", "news_ja.txt", "gpttext_ja.txt"]
ua_files = ["aobun_ua.txt", "nipon_ua.txt", "news_ua.txt", "gpttext_ua.txt"]

data = []
for ja_file, ua_file in zip(ja_files, ua_files):
    with open(ja_file, "r", encoding="utf-8") as ja_f, open(ua_file, "r", encoding="utf-8") as ua_f:
        ja_sentences = ja_f.readlines()
        ua_sentences = ua_f.readlines()

        for ja, ua in zip(ja_sentences, ua_sentences):
            data.append({"ja": ja.strip(), "ua": ua.strip()})

with open("train_dataset.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

dataset = datasets.Dataset.from_list(data)
dataset = dataset.train_test_split(test_size=0.2)
dataset.save_to_disk("ja_ua_dataset")