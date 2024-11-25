# Install required packages
# pip install fastapi uvicorn openai

import openai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# OpenAI API Key setup
openai.api_key = "YOUR_OPENAI_API_KEY"

# Initialize FastAPI app
app = FastAPI(title="EcoExpand AI", description="A compliance and incentive guide powered by Generative AI.",
              version="1.0")


# Request model for FastAPI
class QueryRequest(BaseModel):
    user_query: str
    context: str = None  # Optional context field


# Generate response using OpenAI GPT model
def generate_response(user_query: str, context: str = None) -> str:
    """
    Generates a response using OpenAI's GPT model.

    Args:
        user_query (str): The user's query.
        context (str, optional): Optional context for providing specific responses.

    Returns:
        str: The response from the GPT model.
    """
    try:
        # Predefine the system's behavior
        system_prompt = (
            "You are EcoExpand AI, a smart chatbot that helps users understand compliance regulations "
            "and international export incentives. Provide detailed, accurate, and actionable guidance."
        )

        # Append context if provided
        if context:
            system_prompt += f"\nContext: {context}"

        # Call OpenAI's GPT-4 API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            max_tokens=300,  # Adjust based on response length requirements
            temperature=0.7  # Controls creativity
        )

        return response['choices'][0]['message']['content']

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")


# API endpoint to handle queries
@app.post("/chat", summary="Chat with EcoExpand AI")
def chat_with_ai(query: QueryRequest):
    """
    Endpoint to interact with the chatbot.

    Args:
        query (QueryRequest): JSON payload containing `user_query` and optional `context`.

    Returns:
        JSON: The chatbot's response.
    """
    try:
        response = generate_response(query.user_query, query.context)
        return {"response": response}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


# Root endpoint
@app.get("/", summary="Welcome to EcoExpand AI")
def root():
    """
    Root endpoint for the API.
    """
    return {"message": "Welcome to EcoExpand AI! Use the /chat endpoint to ask compliance-related questions."}

