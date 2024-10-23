import requests
import json
import time
from datasets import load_dataset
from openai import OpenAI

# Part 1: Data Reading
# Load the dataset
dataset = load_dataset("jonhpark/3kingdoms_qa", split="train")
levels = set(dataset['level'])

# Define number of rows to sample for each level
level_sample_sizes = {
    "easy":5, 
    "medium":5, 
    "hard": 5,
    "very hard": 5,
    "super hard": 5,
}

# Function to sample rows for each level
def sample_rows_for_level(dataset, level, N):
    # Filter dataset for this level
    filtered = dataset.filter(lambda x: x['level'] == level)
    
    # Randomly select N rows or all rows if less than N
    return filtered.shuffle(seed=42).select(range(min(N, len(filtered))))

# Collect samples for each level
sampled_data = {level: sample_rows_for_level(dataset, level, level_sample_sizes.get(level, 5)) for level in levels}

# Part 2: Send Questions to API and Get Responses
# URL for the OpenAI API server
api_url = "http://0.0.0.0:8000/test"
headers = {"Content-Type": "application/json"}

# Function to send a POST request and parse the response
def curl_and_parse(url, headers, data):
    start_time = time.time()
    response = requests.post(url, headers=headers, data=json.dumps(data))
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"API response time: {elapsed_time:.2f} seconds")
    parsed_response = json.loads(response.text)
    return parsed_response

# Collect responses for each question
responses = {}
for level, level_data in sampled_data.items():
    level_responses = []
    for data in level_data:
        question = data["question"]
        print(f"Level: {level}, Question: {question}")
        response = curl_and_parse(api_url, headers, {"text": question})
        print(f"Answer: {data['answer']}")
        print(f"Response: {response['response']}")
        level_responses.append({"question": question, "answer": response["response"], "ground_truth": data["answer"]})
    responses[level] = level_responses

# Part 3: Evaluate Responses
# Modify OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://192.168.233.143:8000/v1"
client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

# Function to call LLM for grading the answer
def call_llm_judge(question, answer, ground_truth):
    prompt = f"""Score the student answer as either CORRECT or INCORRECT.

Example Format:
QUESTION: question here
STUDENT ANSWER: student's answer here
TRUE ANSWER: true answer here
GRADE: CORRECT or INCORRECT here

Grade the student answers based ONLY on their factual accuracy. Ignore differences in punctuation and phrasing between the student answer and true answer.
It is OK if the student answer contains more information than the true answer, as long as it does not contain any conflicting statements. Begin! 

QUESTION: {question}
STUDENT ANSWER: {answer}
TRUE ANSWER: {ground_truth}
GRADE:"""

    chat_response = client.chat.completions.create(
        model="Qwen/Qwen2.5-7B-Instruct",
        messages=[
            {"role": "system", "content": "You are a Teacher to grade your student's answer."},
            {"role": "user", "content": prompt},
        ]
    )

    judge = chat_response.choices[0].message.content.strip()
    return False if "INCORRECT" in judge else True

# Function to evaluate the answer
def evaluate(question, answer, ground_truth):
    if answer == ground_truth:
        return True
    else:
        # Evaluate the answer by LLM
        return call_llm_judge(question, answer, ground_truth)

# Evaluate all responses and calculate the average score for each level
for level, level_responses in responses.items():
    correct_count = 0
    for response in level_responses:
        is_correct = evaluate(response["question"], response["answer"], response["ground_truth"])
        print(f"""Question: {response['question']},
                Answer: {response['answer']},
                Ground Truth: {response['ground_truth']},
                Correct: {is_correct}""")
        if is_correct:
            correct_count += 1
    average_score = correct_count / len(level_responses)
    print(f"Level: {level}, Average Score: {average_score * 100:.2f}%")
