import os
from openai import OpenAI
import json
import logging
import dotenv

dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OPENAI_MODELS = [
    "text-embedding-3-small",
    "text-embedding-3-large",
    "text-embedding-3-large"
]

class OpenAIEmbedding:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": (OPENAI_MODELS, ),
                "input_text": ("STRING", {"multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("response",)
    FUNCTION = "api_call"
    CATEGORY = "embedding"

    def api_call(self, model, input_text):
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        
        if not openai_api_key:
            logger.info("OpenAI API key not set")
            return "OpenAI API key not set"
        
        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
        
        try:
            response = client.embeddings.create(
                input=input_text,
                model=model,
            )
            
            logger.info(response)           
            full_response = response.data[0].embedding
                
            logger.info(full_response)
            return (full_response, )
        except Exception as e:
            error_msg = f"Error during API call: {str(e)}"
            logger.error(error_msg)
            return (error_msg, )