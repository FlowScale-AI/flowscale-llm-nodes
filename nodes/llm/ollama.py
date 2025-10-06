"""
Ollama API Node for ComfyUI

Available Ollama API Options (options passed to the model):
- seed: Random seed for reproducibility (int)
- num_predict: Max number of tokens to generate, -1 for unlimited (int)
- top_k: Reduces probability of generating nonsense. Higher = more diverse (int, default: 40)
- top_p: Works with top-k. Higher = more diverse (float, default: 0.9)
- temperature: Controls randomness. Higher = more creative, lower = more focused (float, default: 0.8)
- repeat_penalty: Penalizes repetition. Higher = less repetition (float, default: 1.1)
- num_ctx: Context window size (int, default: 2048)
- num_keep: Number of tokens to keep from prompt (int)
- typical_p: Typical probability sampling (float)
- repeat_last_n: Look back N tokens for repeat penalty (int)
- presence_penalty: Penalizes new tokens based on presence in text (float)
- frequency_penalty: Penalizes new tokens based on frequency in text (float)
- penalize_newline: Penalize newlines in output (bool)
- stop: Stop sequences (array of strings)
- numa: Enable NUMA support (bool)
- main_gpu: Main GPU index (int)
- use_mmap: Use memory mapping (bool)
- num_thread: Number of threads (int)

This node includes the most commonly used options. For full documentation, see:
https://github.com/ollama/ollama/blob/main/docs/api.md
"""

import logging
import requests
import dotenv

dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OLLAMA_MODELS = [
    "llama3.1:8b-instruct-q8_0",
    "mistral:7b",
    "deepseek-r1:8b",
    # "gpt-oss:latest",
]

class OllamaAPI:
    """
    A node for calling Ollama API to generate LLM responses.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_endpoint": ("STRING", {"default": "http://localhost:11434/api/generate"}),
                "model": (OLLAMA_MODELS, ),
                "prompt": ("STRING", {"multiline": True}),
                "response_format": (["text", "json"], ),
                "temperature": ("FLOAT", {"default": 0.8, "min": 0.0, "max": 2.0, "step": 0.01}),
            },
            "optional": {
                "system_prompt": ("STRING", {"default": "", "multiline": True}),
                "seed": ("INT", {"default": 42, "min": 0, "max": 999999}),
                "top_k": ("INT", {"default": 20, "min": 0, "max": 100}),
                "top_p": ("FLOAT", {"default": 0.9, "min": 0.0, "max": 1.0, "step": 0.01}),
                "repeat_penalty": ("FLOAT", {"default": 1.1, "min": 0.0, "max": 2.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("response",)
    FUNCTION = "api_call"
    CATEGORY = "llm"

    def api_call(
        self,
        api_endpoint,
        model,
        prompt,
        response_format,
        temperature,
        system_prompt="",
        seed=42,
        top_k=20,
        top_p=0.9,
        repeat_penalty=1.1,
    ):
        if not prompt or prompt.strip() == "" or prompt == "exit":
            return (None, )

        # Build the request payload
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "seed": seed,
                "top_k": top_k,
                "top_p": top_p,
                "temperature": temperature,
                "repeat_penalty": repeat_penalty,
            }
        }

        # Add system prompt if provided
        if system_prompt and system_prompt.strip():
            payload["system"] = system_prompt

        # Set response format
        if response_format == "json":
            payload["format"] = "json"

        try:
            logger.info(f"Calling Ollama API at {api_endpoint} with model {model}")

            response = requests.post(
                api_endpoint,
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=300  # 5 minute timeout for long responses
            )

            response.raise_for_status()
            response_data = response.json()

            logger.info(f"Ollama response received: {response_data}")

            # Extract the response text
            full_response = response_data.get("response", "").strip()

            if not full_response:
                error_msg = "No response received from Ollama API"
                logger.error(error_msg)
                return (error_msg, )

            logger.info(f"Ollama response: {full_response}")
            return (full_response, )

        except requests.exceptions.Timeout:
            error_msg = "Request to Ollama API timed out"
            logger.error(error_msg)
            return (error_msg, )
        except requests.exceptions.RequestException as e:
            error_msg = f"Error during Ollama API call: {str(e)}"
            logger.error(error_msg)
            return (error_msg, )
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            return (error_msg, )
