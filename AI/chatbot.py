import openai

# API Key setup
openai.api_key = "YOUR_OPENAI_API_KEY"

def generate_response(user_query, context=None):
    try:
        # Predefine the system's behavior
        system_prompt = (
            "You are EcoExpand AI, a smart chatbot that helps users understand compliance regulations "
            "and international export incentives. Provide detailed, accurate, and actionable guidance."
        )
        
        # Call OpenAI's GPT-4 API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            max_tokens=300,  # Adjust token limit based on response length requirements
            temperature=0.7  # Controls creativity (higher = more creative)
        )
        
        # Extract and return the assistant's reply
        return response['choices'][0]['message']['content']
    
    except Exception as e:
        return f"Error generating response: {str(e)}"

def chatbot():
    print("EcoExpand AI: Your compliance and incentive guide.\n(Type 'exit' to end the session.)\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("EcoExpand AI: Goodbye! Have a great day!")
            break
        
        # Generate and print the response
        response = generate_response(user_input)
        print(f"EcoExpand AI: {response}\n")

# Run the chatbot
if __name__ == "__main__":
    chatbot()
