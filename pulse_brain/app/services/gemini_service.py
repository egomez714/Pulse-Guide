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
        You are an AI Body Cam Assistant for a First Responder.
        
        CONTEXT: 
        The camera is strapped to the rescuer's chest (Ego-centric view).
        You will see the patient's chest and the rescuer's arms extending forward.
        
        TASK:
        Analyze the CPR mechanics from this POV.
        
        1. RECOIL CHECK: Watch the rescuer's arms. If they don't pull back enough, the camera won't move up.
        2. DEPTH CHECK: If the camera doesn't shake/move rhythmically, compressions are too shallow.
        3. SCENE SCAN: Look for "Scene Safety" issues in the periphery (fire, weapons, gas).
        
        OUTPUT (JSON):
        {
          "thought_process": "POV shows low vertical displacement. Arms obstructing view of sternum. Rate is consistent.",
          "haptic_feedback": true,  // Should phone vibrate?
          "audio_command": "PUSH DEEPER" // Short, loud commands only
        }
        """
    async def analyze_frame(self,image_bytes: bytes):
        
        try:
            # creates a seperate thread for the google API call
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=self.model_id,
                contents=[
                    # converts image for AI to understand
                    Part.from_bytes(data=image_bytes,mime_type="image/jpeg"),
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
            return '{"audio_command": "ERROR", "haptic_feedback": false, "thought_process": "System Failure"}'