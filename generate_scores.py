import os
import re
import json
from datetime import datetime
from pprint import pprint
import sys

import bitsandbytes as bnb
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from datasets import load_dataset

# from peft import (
#     LoraConfig,
#     PeftConfig,
#     PeftModel,
#     get_peft_model,
#     prepare_model_for_kbit_training,
# )
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)

from prompts.en.zs_prompt import BASE_PROMPT as zs
from prompts.en.fs_prompt import BASE_PROMPT as fs, CONTENT_PROMPT
from prompts.en.ct_prompt import BASE_PROMPT as ct
from check_llm_answer import load_annotated_pair_of_sentences, TEST_DATA_EN


def extract_number(text: str):
    pattern = r"\b\d+\b"
    numbers = re.findall(pattern, text)

    try:
        return numbers[0]
    except Exception as e:
        return None


model_name = "mistralai/Mixtral-8x7B-Instruct-v0.1"
path_to_data = "dwug_en/data"
PROMPTS = {"zs": zs, "fs": fs, "ct": ct}
sentences_per_target_word = load_annotated_pair_of_sentences(path_to_data)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    quantization_config=bnb_config,
    trust_remote_code=True,
)
model.config.use_cache = False
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token

generation_config = model.generation_config
generation_config.max_new_tokens = 20
generation_config.temperature = 0.7
generation_config.top_p = 0.7
generation_config.num_return_sequences = 1
generation_config.pad_token_id = tokenizer.eos_token_id
generation_config.eos_token_id = tokenizer.eos_token_id

output = "outputs/mixtral-8xtb-v0.1/dwug_en/{folder}"
start_time_experiments = datetime.now()

for prompt in PROMPTS.keys():
    for index, word in enumerate(TEST_DATA_EN):
        start_time = datetime.now()
        df = sentences_per_target_word[word]
        score_per_sentence_pair = []
        index = 0

        for row in df:
            sentence1 = row.sentence1
            sentence2 = row.sentence2
            target_word = word

            device = "cuda:1"
            prompt_filled = PROMPTS[prompt]["content"].format(
                target_word=target_word, sentence1=sentence1, sentence2=sentence2
            )
            largo = len(prompt_filled)
            encoding = tokenizer(prompt_filled, return_tensors="pt").to(device)
            with torch.inference_mode():
                outputs = model.generate(
                    input_ids=encoding.input_ids,
                    attention_mask=encoding.attention_mask,
                    generation_config=generation_config,
                )
            aux = tokenizer.decode(outputs[0], skip_special_tokens=True)
            aux = aux[largo:].strip()
            aux = extract_number(aux)
            print(aux)

            score_per_sentence_pair.append(
                {
                    "identifier1": row.identifier1,
                    "identifier2": row.identifier2,
                    "score": "-" if aux is None else aux,
                }
            )
            print(f"processing pair of sentence No: {index + 1}/{len(df)}")
            index += 1

        with open(f"{output.format(folder=prompt)}/dev.{word}.scores", "w") as f_out:
            json.dump(score_per_sentence_pair, f_out)

        print(f"{word}: Elapsed time {datetime.now() - start_time}")

print(f"General elapsed time: {datetime.now() - start_time_experiments}")
