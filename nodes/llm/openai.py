import os
from openai import OpenAI
import json
import logging
import dotenv

dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OPENAI_MODELS = [
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0125",
    "gpt-4",
    "gpt-4-turbo",
    "gpt-4o-mini",
    "gpt-4o",
    "o1",
    "o1-mini",
    "o1-preview",
]

class OpenAIAPI:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": (OPENAI_MODELS, ),
                "system_prompt": ("STRING", {"default": "You are a helpful assistant.", "multiline": True}),
                "prompt": ("STRING", {"multiline": True}),
                "response_format": (["text", "json_object"], ),
                "temperature": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.01}),
                "top_p": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "max_completion_tokens": ("INT", {"default": 100, "min": 0, "max": 4000}),
                "presence_penalty": ("FLOAT", {"default": 0.0, "min": -2.0, "max": 2.0, "step": 0.01}),
                "frequency_penalty": ("FLOAT", {"default": 0.0, "min": -2.0, "max": 2.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("response",)
    FUNCTION = "api_call"
    CATEGORY = "llm"

    def api_call(self, model, system_prompt, prompt, response_format, temperature, top_p, max_completion_tokens, presence_penalty, frequency_penalty):
        if prompt == "" or prompt == "exit" or prompt == None:
            return (None, )
        
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        
        if not openai_api_key:
            logger.info("OpenAI API key not set")
            return "OpenAI API key not set"
        
        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
        
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                  {"role": "system", "content": system_prompt},
                  {"role": "user", "content": prompt}
                ],
                response_format={
                  "type": response_format
                },
                temperature=temperature,
                top_p=top_p,
                max_completion_tokens=max_completion_tokens,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty,
            )
            
            logger.info(response)           
            full_response = response.choices[0].message.content.strip()
                
            logger.info(full_response)
            return (full_response, )
        except Exception as e:
            error_msg = f"Error during API call: {str(e)}"
            logger.error(error_msg)
            return (error_msg, )