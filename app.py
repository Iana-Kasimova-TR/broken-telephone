import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="LLM Broken Telephone Game API")


class GameRequest(BaseModel):
    start_prompt: str
    n_rounds: int = 3


class LLMBrokenTelephoneGame:
    def __init__(self, n_rounds):
        self.n_rounds = n_rounds
        self.client = OpenAI(
            api_key=os.environ.get("NEBIUS_API_KEY"),
            base_url="https://api.studio.nebius.ai/v1/",
        )

    def play_game(self, start_prompt):
        images = []
        prompts = []
        counter = 0
        prompt = start_prompt

        while counter < self.n_rounds:
            try:
                response = self.client.images.generate(
                    model="black-forest-labs/flux-dev",
                    response_format="b64_json",
                    extra_body={
                        "response_extension": "png",
                        "width": 1024,
                        "height": 1024,
                        "num_inference_steps": 28,
                        "negative_prompt": "",
                        "seed": -1,
                    },
                    prompt=prompt,
                )
                response_json = response.to_json()
                response_data = json.loads(response_json)
                b64_image = response_data["data"][0]["b64_json"]
                images.append(b64_image)

                completion = self.client.chat.completions.create(
                    model="Qwen/Qwen2-VL-72B-Instruct",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "please catch the main idea of the following image and describe it in a few words",
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{b64_image}"
                                    },
                                },
                            ],
                        }
                    ],
                )

                prompt = completion.choices[0].message.content
                prompts.append(prompt)
                counter += 1
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        return {"images": images, "prompts": prompts}


@app.post("/play")
async def play_game(request: GameRequest):
    game = LLMBrokenTelephoneGame(request.n_rounds)
    result = game.play_game(request.start_prompt)
    return result


@app.get("/")
async def root():
    return {"message": "Welcome to the LLM Broken Telephone Game API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
