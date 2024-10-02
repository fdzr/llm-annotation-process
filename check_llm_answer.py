import copy
import csv
from datetime import datetime
import logging
import itertools
from typing import List
from pathlib import Path
from collections import namedtuple
from pprint import pprint
import sys
import unicodedata

import pandas as pd
from huggingface_hub import login


login(token="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")
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)


PATH = "dwug_es/data"
TARGET_WORDS = ["banco", "pila", "disco"]
TEST_DATA = pd.read_csv(
    "test_data.csv",
    sep="\t",
    engine="python",
    on_bad_lines="warn",
    quoting=csv.QUOTE_NONE,
    encoding="utf-8",
).word.to_list()
Uses = namedtuple("Uses", ["sentence1", "sentence2", "identifier1", "identifier2"])

with open("dwug_en/target_words.txt", "r") as f_in:
    TEST_DATA_EN = f_in.read().split("\n")


def load_data(path: str, pattern: str = "*/*uses.csv") -> dict[str, pd.DataFrame]:
    logging.info("loading data ...")
    ans = {}
    path_to_uses = Path(path)
    paths = [*path_to_uses.glob(pattern)]

    for p in paths:
        data = pd.read_csv(
            p,
            sep="\t",
            engine="python",
            on_bad_lines="warn",
            quoting=csv.QUOTE_NONE,
            encoding="utf-8",
        )

        ans[unicodedata.normalize("NFC", p.parts[-2])] = data

    logging.info("data loaded ...")

    return ans


def load_ids_from_sentences(judgments: pd.DataFrame):
    ids = set([item for item in zip(judgments.identifier1, judgments.identifier2)])

    return ids


def find_sentence_by_id(id: str, uses: pd.DataFrame):
    mask = uses.identifier == id
    sentence = uses[mask].context.item()

    return sentence


def create_pair_of_sentences():
    uses = load_data(None, "uses.csv")
    judgments = load_data(None, "judgments.csv")
    ans = {}

    for tw in TARGET_WORDS:
        output = []
        ids = load_ids_from_sentences(judgments[tw])

        for item in ids:
            sentence1 = find_sentence_by_id(item[0], uses[tw])
            sentence2 = find_sentence_by_id(item[1], uses[tw])
            output.append(
                Uses(
                    sentence1=sentence1,
                    sentence2=sentence2,
                    identifier1=item[0],
                    identifier2=item[1],
                )
            )

        ans[tw] = output.copy()

    return ans


def generate_combinations(path_to_data: str, data: dict[str, pd.DataFrame]):
    logging.info("generating combinations ...")
    ans = {}

    for tw in TEST_DATA_EN:
        ids = data[tw].identifier
        ans[tw] = [*itertools.combinations(ids, 2)]

    logging.info("combinations generated ...")

    return ans


def create_pair_of_sentences_from_combinations(path_to_data: str):
    uses = load_data(path_to_data)
    combinations = generate_combinations(path_to_data, uses)
    ans = {}

    logging.info("saving combinations of sentence pairs")

    now = datetime.now()
    for tw in TEST_DATA_EN:
        output = []
        for id1, id2 in combinations[tw]:
            sentence1 = find_sentence_by_id(id1, uses[tw])
            sentence2 = find_sentence_by_id(id2, uses[tw])
            output.append(
                Uses(
                    sentence1=sentence1,
                    sentence2=sentence2,
                    identifier1=id1,
                    identifier2=id2,
                )
            )

        ans[tw] = copy.deepcopy(output)

    logging.info("combinations of sentence pairs saved ...")
    logging.info(f"elapsed time saving sentence pairs: {datetime.now() - now}")

    return ans


def load_annotated_pair_of_sentences(path_to_data: str):
    uses = load_data(path_to_data)
    judgments = load_data(path_to_data, "*/*judgments.csv")
    ans = {}

    logging.info("saving annotated sentences from users ...")

    now = datetime.now()
    for tw in TEST_DATA_EN:
        output = []

        judgment = judgments[tw]
        ids = judgment.apply(
            lambda row: tuple(sorted([row["identifier1"], row["identifier2"]])), axis=1
        )
        ids = set(ids.values)

        for id1, id2 in ids:
            sentence1 = find_sentence_by_id(id1, uses[tw])
            sentence2 = find_sentence_by_id(id2, uses[tw])
            output.append(
                Uses(
                    sentence1=sentence1,
                    sentence2=sentence2,
                    identifier1=id1,
                    identifier2=id2,
                )
            )

        ans[tw] = copy.deepcopy(output)

    logging.info("annotated sentences from users saved ...")
    logging.info(f"elapsed time saving sentence pairs: {datetime.now() - now}")

    return ans


if __name__ == "__main__":
    load_annotated_pair_of_sentences("dwug_en/data")
