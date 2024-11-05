import json
import openai
import os
from typing import List, Dict
import time

# Load OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def read_jsonl(file_path: str) -> List[Dict]:
    """Read jsonl file and return list of dictionaries."""
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data

def get_similarity_score(generated: str, ground_truth: str) -> float:
    """Use GPT-4 to evaluate similarity between generated and ground truth descriptions."""
    prompt = f"""
    On a scale of 0-10, how similar are these two descriptions in terms of their core meaning and key details?

    Description 1: {generated}
    Description 2: {ground_truth}

    Provide only a numeric score where:
    0 = Completely different/unrelated
    10 = Identical in meaning and key details

    Score:"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        score_text = response.choices[0].message.content.strip()
        try:
            score = float(score_text)
            return min(max(score, 0), 10)  # Ensure score is between 0-10
        except ValueError:
            print(f"Could not parse score from response: {score_text}")
            return 0
    except Exception as e:
        print(f"Error getting similarity score: {e}")
        return 0

def evaluate_descriptions(evals_file: str):
    """Evaluate similarity between generated and ground truth descriptions."""
    data = read_jsonl(evals_file)
    scores = []

    for i, entry in enumerate(data):
        generated = entry.get('generated_description', '')
        ground_truth = entry.get('ground_truth', '')

        if not generated or not ground_truth:
            continue

        print(f"\nEvaluating entry {i+1}/{len(data)}")
        score = get_similarity_score(generated, ground_truth)
        scores.append(score)
        print(f"Score: {score}/10")

        # Add delay to avoid rate limiting
        time.sleep(1)

    # Calculate and print aggregate statistics
    if scores:
        avg_score = sum(scores) / len(scores)
        print(f"\nEvaluation Results:")
        print(f"Number of evaluations: {len(scores)}")
        print(f"Average similarity score: {avg_score:.2f}/10")
        print(f"Min score: {min(scores)}/10")
        print(f"Max score: {max(scores)}/10")

if __name__ == "__main__":
    evaluate_descriptions("evals.jsonl")
