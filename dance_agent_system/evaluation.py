import os
import asyncio
from dotenv import load_dotenv
from google.adk.models.google_llm import Gemini
from google.genai import types

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

retry_config = types.HttpRetryOptions(
    attempts=3,
    exp_base=2,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

model = Gemini(model="gemini-2.5-flash", retry_options=retry_config)

from google.adk.models.llm_request import LlmRequest

async def evaluate_agent_output():
    print("--- Starting Agent Evaluation (LLM-as-a-Judge) ---")
    
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    
    try:
        with open(os.path.join(data_dir, "opportunities_found.txt"), "r") as f:
            opportunities = f.read()
        with open(os.path.join(data_dir, "applications_drafted.txt"), "r") as f:
            applications = f.read()
    except FileNotFoundError:
        print("Error: Output files not found. Run main.py first.")
        return

    prompt_text = f"""
    You are an expert judge evaluating the performance of a Dance Agent System.
    
    TASK:
    Evaluate the quality of the following agent outputs based on:
    1. Relevance: Are the opportunities actually related to Kuchipudi dance?
    2. Completeness: Do the applications include necessary details?
    3. Professionalism: Is the tone appropriate?
    
    --- DATA START ---
    OPPORTUNITIES FOUND:
    {opportunities[:2000]}... (truncated)
    
    APPLICATIONS DRAFTED:
    {applications[:2000]}... (truncated)
    --- DATA END ---
    
    OUTPUT FORMAT:
    Score: [0-10]
    Feedback: [Your detailed feedback here]
    """
    
    print("Sending evaluation request to LLM!!!")
    request = LlmRequest(prompt=prompt_text)
    response_text = ""
    async for chunk in model.generate_content_async(request):
        response_text += chunk.text
        
    print("\n=== EVALUATION REPORT ===")
    print(response_text)

if __name__ == "__main__":
    asyncio.run(evaluate_agent_output())
