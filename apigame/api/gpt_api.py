import json
import logging
from typing import Iterable, Any

from openai import OpenAI

from apigame.services.question import Question

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

API_KEY = ("sk-proj-BgB1dxVD7AivzRfLEOdO7FZZcXAX6VSXNuz1m6xHn4HgN2XDoc_Wtvz-c9bE0W"
           "-sSzxtTNOiSKT3BlbkFJ_ZhKMEfyirahx5j3PkU5B23hQFzFXzigGtUjk216WrYmw7rbaHJJotnEQDOXYXlH76G7cIncsA")

PROMPT = """
Translate the provided list of quiz questions from American English into Brazilian Portuguese. Maintain the original structure and formatting, ensuring proper nouns remain intact. Add a "hint" field to assist in finding the correct answer.

# Instructions

- Translate the following fields into Brazilian Portuguese:
  - Question text
  - Correct and incorrect answers
  - Category
- Retain the structural and formatting integrity of the original questions.
- Keep proper nouns (e.g., names of places, brands) unchanged.

# Output Format

The output should maintain the same JSON structure as the input. Translate relevant fields into Brazilian Portuguese, and include an additional "hint" string field in each question object.

# Notes

- Pay attention to cultural nuances in the translation, ensuring local relevance.
- Do not modify the original formatting, structure, or any identifier tags in the JSON.

# Steps

1. Identify and translate relevant fields while keeping the structure intact.
2. Verify the accuracy of the proper noun handling, ensuring they remain unchanged.
3. Create and append a relevant "hint" field for each question to assist with the answer.

# Examples

**Input:**
```json
{
  "question": "What is the capital of France?",
  "correct_answer": "Paris",
  "incorrect_answers": ["Rome", "Madrid", "Berlin"],
  "category": "Geography"
}
```

**Output:**
```json
{
  "question": "Qual é a capital da França?",
  "correct_answer": "Paris",
  "incorrect_answers": ["Roma", "Madri", "Berlim"],
  "category": "Geografia",
  "hint": "É conhecida como a cidade das luzes."
}
```
"""


class ChatGPTClient:
    def __init__(self):
        """
        Initializes the ChatGPTClient with the provided OpenAI API key.
        """
        logging.debug("Initializing ChatGPTClient")
        self.api_key: str = API_KEY
        self.model: str = "gpt-4o-mini"
        self.client = OpenAI(api_key=self.api_key)
        logging.debug("ChatGPTClient initialized with model '%s'", self.model)

    def generate_translated_and_hinted_questions(self, questions: Iterable[Question]) -> list[Question]:
        """
        Translates the provided questions and generates additional hint questions
        using OpenAI's GPT model.
        """
        logging.info("Generating translated and hinted questions for %d questions", len(questions))

        try:
            # Sending request to OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": PROMPT
                    },
                    {
                        "role": "user",
                        "content": str(questions)
                    }
                ],
                response_format={
                    "type": "json_object"
                },
                temperature=1,
                max_completion_tokens=10000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            logging.debug("Received response from OpenAI API")

            # Extracting response data
            response_content = response.choices[0].message.content
            response_data = json.loads(response_content)
            translated_questions: list[dict[str, Any]] = response_data.get("questions", [])

            logging.info("Successfully translated %d questions", len(translated_questions))

            # Convert dicts to Question objects
            typed_questions: list[Question] = [
                Question(
                    category=question["category"],
                    difficulty=question["difficulty"],
                    type=question["type"],
                    question=question["question"],
                    correct_answer=question["correct_answer"],
                    incorrect_answers=question["incorrect_answers"],
                    hint=question["hint"]
                ) for question in translated_questions
            ]

            logging.debug("Returning %d typed questions", len(typed_questions))
            return typed_questions

        except Exception as e:
            logging.error("An error occurred while generating translated questions: %s", e)
            raise
