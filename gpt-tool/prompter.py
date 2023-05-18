import openai
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set the API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable not set")

openai.api_key = openai_api_key

logger = logging.getLogger("prompter")

MODEL_NAME = "gpt-3.5-turbo"


def call_chatgpt(code):
    prompt = (
        f"Given performance issues:\n\n"
        f"Computational Expensive Operation\n"
        f"Inefficient Data Structures\n"
        f"Not Using Function Inlining\n"
        f"Inefficient Concurrency Control\n"
        f"Missing SIMD Parallelism\n"
        f"Missing GPU Parallelism\n"
        f"Missing Task Parallelism\n\n"
        f"Detect and classify performance-related bugs in given C++ code - which can be sequential, OpenMP-based (CPU parallel) or CUDA-based (GPU Parallel)."
        f"Only use the classes that are given and ONLY USE THE FORMAT BELOW\n"
        f"Computational Expensive Operation: {{ YOUR ANSWER }}"
        f"\n...\n\n"
        f"given code:\n{code}"
    )
    logger.log(0, msg=f"PROMPT: {prompt}")

    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        temperature=0.1,
        n=1,
        messages=[
            {
                "role": "system",
                "content": "You are a HPC expert who can analyze parallel and sequential code and classify performance bugs.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    result = response["choices"][0]["message"]["content"]
    logger.log(0, f"RESPONSE: {result}")

    # Split the response into separate parts for each issue
    issues = result.split("\n")
    issues_dict = {}
    for issue in issues:
        if ": " in issue:
            key, val = issue.split(": ", 1)
            issues_dict[key] = val
    return issues_dict

    return result
