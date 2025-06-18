import os
#import cohere
from langchain.llms import cohere

# Load your Cohere API key from environment variable
api_key = "your_cohere_api_key_here"  # Replace with your actual API key or load from env
if not api_key:
    raise ValueError(" COHERE_API_KEY environment variable not found!")

# Initialize Cohere client
#llm = cohere.Cohere(api_key)
llm = cohere.Cohere(cohere_api_key=api_key, temperature=0.1)

# Your test prompt
# Your prompt
prompt_text = "Explain the difference between artificial intelligence and machine learning in simple terms."

# Generate response
response = llm.generate(
    #model="command-light",  # or use "command", "command-light"
    prompts=[prompt_text],   #  prompts expects a list
    max_tokens=300,
    temperature=0.5
)

# Print result
print("\n Cohere Response:")
#print(response.generations[0].text.strip())
print(response)