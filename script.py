import os
import argparse
import json
from datetime import datetime
from openai import OpenAI

def read_system_prompt(filename="systemprompt.md"):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read().strip()

def generate_social_media_posts(num_posts):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ.get("OPENROUTER_API_KEY")
    )

    # Read system prompt from file
    system_prompt = read_system_prompt()

    # Initialize chat history with a system message
    chat_history = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    for i in range(num_posts):
        # Add user message to chat history
        chat_history.append({
            "role": "user",
            "content": f"Generate a creative social media post (number {i+1}). Make sure it's different from the previous posts."
        })

        # Generate completion
        completion = client.chat.completions.create(
            model="anthropic/claude-3.5-sonnet:beta",
            messages=chat_history
        )

        # Extract the generated content
        generated_content = completion.choices[0].message.content

        # Add assistant's response to chat history
        chat_history.append({
            "role": "assistant",
            "content": generated_content
        })

        # Print the generated post
        print(f"Post {i+1}:")
        print(generated_content)
        print()

    return chat_history

def main():
    parser = argparse.ArgumentParser(description="Generate social media posts about Torus using AI")
    parser.add_argument("num_posts", type=int, help="Number of social media posts to generate")
    args = parser.parse_args()

    if "OPENROUTER_API_KEY" not in os.environ:
        print("Error: OPENROUTER_API_KEY environment variable is not set.")
        return

    chat_history = generate_social_media_posts(args.num_posts)

    # Generate a timestamp for the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chat_history_{timestamp}.json"

    # Dump the chat history to a pretty-printed JSON file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(chat_history, f, ensure_ascii=False, indent=2)

    print(f"\nChat history has been saved to {filename}")

if __name__ == "__main__":
    main()
