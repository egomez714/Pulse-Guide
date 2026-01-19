import logging
import asyncio
from google import genai
from google.genai.types import GenerateContentConfig, Part

# imports function from config file for api key
from app.core.config import get_settings

# logging
logger = logging.getLogger("GeminiService")
settings = get_settings()

class GeminiService:
    # handles AI context 
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_id= settings.GEMINI_MODEL_ID
        self.system_instruction = """
        You are a CPR Feedback Algorithm.
        Analyze the image provided.
        1. Identify the hand placement relative to the sternum.
        2. Estimate if the compression looks deep or shallow based on arm angle.
        
        OUTPUT RULES:
        Return a JSON object ONLY. No markdown.
        Format: {"command": "FASTER" | "SLOWER" | "GOOD" | "HANDS LOWER", "reasoning": "..."}
        """
    async def analyze_frame(self,image_bytes: bytes):
        
        try:
            # creates a seperate thread for the google API call
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=self.model_id,
                contents=[
                    # converts image for AI to understand
                    Part.from_bytes(data=image_bytes,mime_types="image/jpeg"),
                    "Analyze this CPR frame."
                ],
                config=GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    response_mime_type="application/json",
                    thinking_config={"include_thoughts":True}
                )
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini API Error: {e}")
            return '{"command": "ERROR"}'