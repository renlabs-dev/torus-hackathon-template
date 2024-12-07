import os
import argparse
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# How many previous chat messages to keep in the context when prompting the model
chat_history_limit = 30

# File to store chat history
chat_history_filename = "chat_history.json"

# The model to use for generating social media posts
model = "grok-beta"

def generate_social_media_posts(num_posts):
    def load_chat_history():
        def read_system_prompt(filename="systemprompt.md"):
            with open(filename, 'r', encoding='utf-8') as file:
                return file.read().strip()

        if not os.path.exists(chat_history_filename):
            # Initialize chat history with a system message
            return [
                {
                    "role": "system",
                    "content": read_system_prompt() # Read system prompt from file
                }
            ]
        with open(chat_history_filename, 'r', encoding='utf-8') as file:
            return json.load(file)

    def write_chat_history(chat_history):
        with open(chat_history_filename, 'w', encoding='utf-8') as file:
            json.dump(chat_history, file, ensure_ascii=False, indent=2)
        print(f"\nChat history has been saved to {chat_history_filename}")

    def trim_chat_history(chat_history, limit):
        if len(chat_history) > limit:
            # Keep the first element and the last (limit - 1) elements
            return [chat_history[0]] + chat_history[-(limit - 1):]
        else:
            # If the chat history is already within the limit, return it unchanged
            return chat_history

    client = OpenAI(
        base_url="https://api.x.ai/v1",
        api_key=os.environ.get("XAI_API_KEY")
    )

    chat_history = load_chat_history()

    for i in range(num_posts):
        # Add user message to chat history
        chat_history.append({
            "role": "user",
            "content": f"Generate a creative social media post. Make sure it's different from the previous posts."
        })

        # Generate completion
        completion = client.chat.completions.create(
            model=model,
            messages=trim_chat_history(chat_history, chat_history_limit)
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

    # Save chat history to file
    write_chat_history(chat_history)

def main():
    parser = argparse.ArgumentParser(description="Generate social media posts about Torus using AI")
    parser.add_argument("num_posts", type=int, help="Number of social media posts to generate")
    args = parser.parse_args()

    if "XAI_API_KEY" not in os.environ:
        print("Error: XAI_API_KEY environment variable is not set.")
        return

    generate_social_media_posts(args.num_posts)

if __name__ == "__main__":
    main()
