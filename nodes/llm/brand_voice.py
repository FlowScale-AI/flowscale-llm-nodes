import os
from openai import OpenAI
import logging
import dotenv

dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OPENAI_MODELS = [
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-turbo",
    "gpt-4o"
]

BRAND_VOICES = [
  "Cheerful",
  "Professional",
  "Friendly",
  "Inquisitive",
  "Sarcastic",
  "Formal",
  "Casual",
  "Direct",
  "Informative",
  "Inspirational",
  "Persuasive",
  "Technical",
  "Humorous",
  "Empathetic",
  "Caring",
  "Confident",
  "Assertive",
  "Respectful",
  "Authoritative",
  "Enthusiastic",
  "Energetic",
  "Sincere",
  "Curious",
  "Helpful",
  "Supportive",
  "Playful",
  "Imaginative",
  "Creative",
  "Bold",
  "Daring",
  "Adventurous",
  "Optimistic",
  "Motivational",
  "Encouraging",
  "Inspiring",
  "Challenging",
  "Reassuring",
  "Comforting",
  "Relatable",
  "Approachable",
  "Warm",
  "Welcoming",
  "Inviting",
  "Engaging",
  "Captivating",
  "Compelling",
  "Thoughtful",
  "Considerate",
  "Kind",
  "Gentle",
  "Patient",
  "Understanding",
  "Tolerant",
  "Accepting",
  "Resilient",
  "Persistent",
  "Determined",
  "Focused",
  "Driven",
  "Ambitious",
  "Passionate",
  "Dedicated",
  "Devoted",
  "Loyal",
  "Committed",
  "Trustworthy",
  "Honest",
  "Transparent",
  "Authentic",
  "Genuine",
]

class OpenAIBrandVoiceReformatter:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": (OPENAI_MODELS, ),
                "brand_voice": (BRAND_VOICES, ),
                "prompt": ("STRING", {"multiline": True}),
                "temperature": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.01}),
                "max_completion_tokens": ("INT", {"default": 100, "min": 0, "max": 4000}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("response",)
    FUNCTION = "api_call"
    CATEGORY = "llm"

    def api_call(self, model, brand_voice, prompt, temperature, max_completion_tokens):
        if prompt == "" or prompt == "exit" or prompt == None:
            return (None, )
        
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        
        if not openai_api_key:
            logger.info("OpenAI API key not set")
            return "OpenAI API key not set"
        
        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
        
        system_prompt = f"""
          You are a highly skilled language model specialized in adjusting tones and voices of content. Your task is to reformat and rewrite the provided text in a clear, coherent, and engaging way that aligns with the specified brand voice. Ensure that the restructured text stays true to the original message while reflecting the desired tone. 

          Brand Voice: {brand_voice}

          Guidelines:
          - Respect the structure and key points of the original text.
          - Use vocabulary, phrasing, and sentence style that align with the chosen voice.
          - Make the tone consistent throughout the response.

          Reformat the following text:
        """
        
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                  {"role": "system", "content": system_prompt},
                  {"role": "user", "content": prompt}
                ],
                response_format={
                  "type": "text"
                },
                temperature=temperature,
                max_completion_tokens=max_completion_tokens,
            )
            
            logger.info(response)           
            full_response = response.choices[0].message.content.strip()
                
            logger.info(full_response)
            return (full_response, )
        except Exception as e:
            error_msg = f"Error during API call: {str(e)}"
            logger.error(error_msg)
            return (error_msg, )