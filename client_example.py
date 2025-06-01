import requests
import base64
from IPython.display import Image, display
import json


def play_game(server_url, start_prompt, n_rounds=3):
    """
    Play the broken telephone game using the API

    Args:
        server_url (str): The URL of the API server
        start_prompt (str): The initial prompt to start the game
        n_rounds (int): Number of rounds to play
    """
    # Make the API request
    response = requests.post(
        f"{server_url}/play", json={"start_prompt": start_prompt, "n_rounds": n_rounds}
    )

    if response.status_code != 200:
        print(f"Error: {response.text}")
        return

    result = response.json()

    # Display the results
    for i, (image_b64, prompt) in enumerate(zip(result["images"], result["prompts"])):
        print(f"\nRound {i + 1}:")
        print(f"Prompt: {prompt}")

        # Display the image
        image_data = base64.b64decode(image_b64)
        display(Image(image_data))


# Example usage in Colab:
"""
# First, install required packages
!pip install requests

# Then run the game
server_url = "http://your-server-url:8000"  # Replace with your server URL
start_prompt = "A beautiful sunset over mountains"
play_game(server_url, start_prompt, n_rounds=3)
"""
