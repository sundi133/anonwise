import spacy
import spacy.displacy
import argparse


def anonymize_string(input_string, start_position, end_position, placeholder="X"):
    if (
        start_position < 0
        or start_position >= len(input_string)
        or end_position < 0
        or end_position >= len(input_string)
    ):
        raise ValueError("Invalid start or end position")

    anonymized_chars = [placeholder] * (end_position - start_position + 1)
    anonymized_string = (
        input_string[:start_position]
        + "".join(anonymized_chars)
        + input_string[end_position + 1 :]
    )

    return anonymized_string


def main():
    parser = argparse.ArgumentParser(
        description="Anonymize and visualize NER entities in text"
    )
    parser.add_argument("text_data", type=str, help="Input text data")
    args = parser.parse_args()

    nlp_ner = spacy.load("model-best")
    text_data = args.text_data
    doc = nlp_ner(text_data)

    colors = {"ADVERTISING_ID": "#F67DE3"}  # Customize entity colors as needed
    options = {"colors": colors}
    entity_size = {"ADVERTISING_ID": 32}  # Customize entity size based on entity label
    print("**Original Text**")
    spacy.displacy.render(doc, style="ent", options=options, jupyter=True)
    for ent in doc.ents:
        start_position_to_anonymize = int(ent.start_char)  # Start position of the range
        end_position_to_anonymize = entity_size[ent.label_]  # End position of the range
        anonymized_result = anonymize_string(
            text_data, start_position_to_anonymize, end_position_to_anonymize
        )
        print("**Redacted Text**")
        print()
        print(anonymized_result)


if __name__ == "__main__":
    main()
