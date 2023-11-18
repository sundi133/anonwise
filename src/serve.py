from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import spacy
import configparser
import os

app = FastAPI()

# Get SpaCy model path from the configuration
spacy_model_path = os.environ["SPACY_MODEL_PATH"]
entity_detection_model = spacy.load(spacy_model_path)


class AnalyzeRequest(BaseModel):
    text: str


class AnonwiseResponse(BaseModel):
    text: str


def get_redacted_data(label):
    """
    Get sample data based on the entity label.

    Args:
    - label (str): The entity label.

    Returns:
    - str: redacted data for the specified entity label.
    """
    # You can customize this function to provide different sample data based on the entity label
    if label == "PERSON":
        return "[REDACTED_PERSON]"
    elif label == "LOCATION":
        return "[REDACTED_LOCATION]"
    elif label == "ORG":
        return "[REDACTED_ORG]"
    elif label == "CREDIT_CARD_NUMBER":
        return "[REDACTED_CREDIT_CARD_NUMBER]"
    else:
        # Default placeholder for unknown labels
        return "[REDACTED]"


def get_anonymize_data(label):
    """
    Get sample data based on the entity label.

    Args:
    - label (str): The entity label.

    Returns:
    - str: anonymize data for the specified entity label.
    """
    # You can customize this function to provide different sample data based on the entity label
    if label == "PERSON":
        return "Person ABC"
    elif label == "LOCATION":
        return "Location XYZ"
    elif label == "ORG":
        return "Company XYZ"
    elif label == "CREDIT_CARD_NUMBER":
        return "Credit Card Number xxxx-xxxx-xxxx-xxxx"
    else:
        # Default placeholder for unknown labels
        return "Anonymize Data {label}"


@app.get("/")
async def root():
    return {"message": "pong"}


@app.post("/redact", response_model=AnonwiseResponse)
async def redact_text(request: AnalyzeRequest):
    try:
        chunks = []
        last_end = 0
        # Process the input text using the SpaCy model
        doc = entity_detection_model(request.text)
        entities = [
            {"start": ent.start_char, "end": ent.end_char, "label": ent.label_}
            for ent in doc.ents
        ]

        original_text = request.text
        for entity in entities:
            start = entity["start"]
            end = entity["end"]
            replacement = get_redacted_data(entity["label"])
            chunks.append(original_text[last_end:start])
            chunks.append(replacement)
            last_end = end
        chunks.append(original_text[last_end:])
        return AnonwiseResponse(text=" ".join(chunks))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.post("/anonymize", response_model=AnonwiseResponse)
async def anonymize_text(request: AnalyzeRequest):
    try:
        # Process the input text using the SpaCy model
        doc = entity_detection_model(request.text)
        entities = [
            {"start": ent.start_char, "end": ent.end_char, "label": ent.label_}
            for ent in doc.ents
        ]

        chunks = []
        last_end = 0
        # Process the input text using the SpaCy model
        doc = entity_detection_model(request.text)
        entities = [
            {"start": ent.start_char, "end": ent.end_char, "label": ent.label_}
            for ent in doc.ents
        ]

        original_text = request.text
        redacted_text = ""
        for entity in entities:
            start = entity["start"]
            end = entity["end"]
            replacement = get_anonymize_data(entity["label"])
            chunks.append(original_text[last_end:start])
            chunks.append(replacement)
            last_end = end
        chunks.append(original_text[last_end:])

        return AnonwiseResponse(text=" ".join(chunks))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
