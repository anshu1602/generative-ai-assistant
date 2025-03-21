import os
from dotenv import load_dotenv
import google.generativeai as genai
from typing import Tuple

# Load API key from .env file
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    print("Error: GOOGLE_API_KEY not found in .env file")
    exit(1)

# Configure Google Generative AI
genai.configure(api_key=google_api_key)

def is_inappropriate(text: str) -> bool:
    """
    A simple content filter to detect potentially inappropriate content.
    """
    inappropriate_terms = [
        "profanity", "obscenity", "hate speech", "violence", "abuse",
        "explicit", "illegal", "harmful", "attack", "weapon"
    ]
    
    text_lower = text.lower()
    for term in inappropriate_terms:
        if term in text_lower:
            return True
    return False

def generate_response(user_query: str) -> Tuple[str, bool]:
    """
    Generate a response using Google's Gemini API and check for inappropriate content.
    """
    if is_inappropriate(user_query):
        return "I'm unable to respond to that query as it appears to contain inappropriate content.", True
        
    try:
        # Initialize the model
        model = genai.GenerativeModel("gemini-1.5-pro")  # Adjust model name if needed
        response = model.generate_content(user_query)
        response_text = response.text.strip()
        
        if is_inappropriate(response_text):
            return "I generated a response but it may contain sensitive content. Please rephrase your query.", True
            
        return response_text, False
        
    except Exception as e:
        return f"An error occurred: {str(e)}", True

def main():
    print("Welcome to the AI Assistant (Powered by Google Gemini). Type 'exit' to quit.")
    
    while True:
        user_query = input("\nYour question: ")
        if user_query.lower() in ["exit", "quit", "bye"]:
            print("Thank you for using the AI Assistant. Goodbye!")
            break
            
        response, was_filtered = generate_response(user_query)
        if was_filtered:
            print("\n[FILTERED RESPONSE]")
        print(f"\nAI: {response}")

if __name__ == "__main__":
    main()