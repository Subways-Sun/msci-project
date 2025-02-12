"""Module using OpenAI API to classify literature."""
# pylint: disable=locally-disabled, line-too-long
# from pydantic import BaseModel
from openai import OpenAI
client = OpenAI()

def classify(openai_model, user_message):
    """Function to chat with the AI"""
    completion = client.chat.completions.create(
        model=openai_model,
        messages=[
            {
                "role": "system",
                "content": "You are a scientific paper classifier. Your task is to classify the given abstract of a scientific paper into one of the following categories: 'relevant cathode', 'relevant anode', 'relevant cathode anode', or 'irrelevant'. The classification is based on whether the abstract mainly discusses sodium ion battery electrodes, and if so, whether it discusses cathode, anode, or both. If the abstract is unrelated to the field, or contains only theoretical approaches such as computer simulations (for example, density functional theory), or mainly discusses other types of batteries such as lithium and potassium ion batteries, or is a review article, classify it as 'irrelevant'. If you are not sure, or the abstract contains too little information, classify it as 'irrelevant'. Do not include quotation marks in your response."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )
    return completion.choices[0].message

# Help me generate a system message for gpt-4o. Each user message is an abstract of a scientific paper. I need the model to classify the paper into "relevant", "irrelevant", "cathode", "anode", based on whether the given abstract is relevant to the field of sodium ion battery electrodes, and if so, does the abstract talk about cathode, anode, or both. The response message should be single words, for example, if an abstract is related to cathode, the response should be "relevant cathode", if related to anode, "relevant anode", if both, "relevant cathode anode", if the abstact is unrelated to the field, or it is a review article, "irrelevant". If the response is "irrelevant", there should't be any further classification of cathode or anode

def rephrase(openai_model, user_message):
    """Function to rephrase the user message"""
    completion = client.chat.completions.create(
        model=openai_model,
        messages=[
            {
                "role": "system",
                "content": "You are a scientific paper rephraser. You will be given an abstract of a scientific paper in the field of batteries. Your task is to rephrase the given abstract, retaining every detail in the original abstract. The overall topic cannot be changed, and any data mentioned cannot be altered. Output only the rephrasing of the abstract, do not include any additional information. Keep your response concise and to the point."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )
    return completion.choices[0].message

# Help me generate a system message for gpt-4o. Each user message is an abstract of a scientific paper. I need the model to rephrase the abstract, retaining every detail in the original abstract. The overall topic cannot be changed, any data mentioned cannot be altered.

def extract(openai_model, user_message):
    """Function to rephrase the user message"""

    response_json = {
        "type": "json_schema",
        "json_schema": {
            "name": "sodium_ion_battery_data",
            "schema": {
                "type": "object",
                "properties": {
                    "material": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "material_type": {
                                    "type": "string",
                                    "enum": ["cathode", "anode", "electrolyte"]
                                },
                                "material_name": {"type": "string"},
                                "material_formula": {"type": "string"},
                                "capacity": {
                                    "type": "object",
                                    "properties": {
                                        "value": {"type": "number"},
                                        "unit": {"type": "string"}
                                    },
                                    "required": ["value", "unit"],
                                    "additionalProperties": False
                                },
                                "cycle_life": {
                                    "type": "object",
                                    "properties": {
                                        "value": {"type": "number"},
                                        "unit": {"type": "string"}
                                    },
                                    "required": ["value", "unit"],
                                    "additionalProperties": False
                                }
                            },
                            "required": ["material_type",
                                            "material_name",
                                            "material_formula",
                                            "capacity",
                                            "cycle_life"],
                            "additionalProperties": False
                        }
                    }
                },
                "required": ["material"],
                "additionalProperties": False
            },
            "strict": True
        }
    }

    completion = client.beta.chat.completions.parse(
        model = openai_model,
        messages = [
            {
                "role": "system",
                "content": "You are an expert at structured data extraction. You will be given unstructured text from a research paper and should convert it into the given structure. The paper should focus on electrode or electrolyte materials of sodium ion batteries. Your task is to extract the material information from the given text. The material information includes the material type (cathode, anode, or electrolyte), material name, material formula, capacity (with unit), and cycle life (with unit). Extract these information for each material mentioned in the paper. You should only look at materials used for sodium ion batteries, not for any other type of battery or material. For any information that the paper doesn't mention or if you are not sure, you should assume it to be unknown (for string type) or 0 (for number type)."
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        response_format = response_json
    )
    return completion.choices[0].message.content
