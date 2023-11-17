#!/usr/bin/env python

import spacy
import json
import argparse

from spacy.tokens import Doc
from spacy.util import filter_spans
from spacy.tokens import DocBin
from tqdm import tqdm


def process_data(ner_data):
    training_data = []
    for example in ner_data:
        temp_dict = {}
        temp_dict["text"] = example["text"]
        temp_dict["entities"] = []
        for annotation in example["entities"]:
            start = annotation["start"]
            end = annotation["end"]
            label = annotation["label"].upper()
            temp_dict["entities"].append((start, end, label))
        training_data.append(temp_dict)
    return training_data


def create_doc(nlp, training_example):
    text = training_example["text"]
    labels = training_example["entities"]
    doc = nlp.make_doc(text)
    ents = []
    for start, end, label in labels:
        span = doc.char_span(start, end, label=label, alignment_mode="contract")
        if span is None:
            print("Skipping entity")
        else:
            ents.append(span)
    filtered_ents = filter_spans(ents)
    doc.ents = filtered_ents
    return doc


def main(input_file, output_file):
    # Load your data from the JSON file
    with open(input_file, "r") as f:
        data = json.load(f)

    # Process the data using data_processing.py module
    training_data = process_data(data)

    # Create a blank English spaCy model
    nlp = spacy.blank("en")
    doc_bin = DocBin()

    # Iterate over training data and convert it to DocBin format
    for training_example in tqdm(training_data):
        doc_bin.add(create_doc(nlp, training_example))

    # Save the processed data to the specified output file
    doc_bin.to_disk(output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process NER data and save it in spaCy format"
    )

    parser.add_argument("--input_file", type=str, help="Path to the input JSON file")
    parser.add_argument(
        "--output_file", type=str, help="Path to the output spaCy data file"
    )

    args = parser.parse_args()
    main(args.input_file, args.output_file)
