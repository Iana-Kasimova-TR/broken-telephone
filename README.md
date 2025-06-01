# LLM Broken Telephone Game API

This is a web service implementation of the LLM Broken Telephone Game, where an image is generated from a prompt, then described by an LLM, and the process repeats.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root with your API key:
```
NEBIUS_API_KEY=your_api_key_here
```

## Running the Server

To run the server locally:
```bash
python app.py
```

The server will start on `http://localhost:8000`

## API Endpoints

- `GET /`: Welcome message
- `POST /play`: Play the broken telephone game
  - Request body:
    ```json
    {
        "start_prompt": "your initial prompt",
        "n_rounds": 3  // optional, defaults to 3
    }
    ```
  - Response:
    ```json
    {
        "images": ["base64_encoded_image1", "base64_encoded_image2", ...],
        "prompts": ["prompt1", "prompt2", ...]
    }
    ```

## Using in Colab

1. Copy the contents of `client_example.py` to your Colab notebook
2. Make sure your server is running and accessible
3. Update the `server_url` in the example code
4. Run the example code

## Example Usage

```python
from client_example import play_game

server_url = "http://your-server-url:8000"
start_prompt = "A beautiful sunset over mountains"
play_game(server_url, start_prompt, n_rounds=3)
```

## Notes

- The service uses the Nebius API for image generation
- The Qwen2-VL-72B-Instruct model is used for image description
- Make sure you have the necessary API keys and permissions