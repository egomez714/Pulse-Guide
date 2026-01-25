# allows async/await and threads
import asyncio

# used to parse string from gemini
import json

# for debugging
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.gemini_service import GeminiService

router = APIRouter()
logger = logging.getLogger("CPR_Router")

@router.websocket("/ws/cpr-stream")
async def cpr_websocket(websocket:WebSocket):
    
    await websocket.accept()
    gemini_service = GeminiService()
    logger.info("Flutter connected")
    
    try:
        while True:

            #receives image
            data = await websocket.receive_bytes()
            
            #send image to gemini 
            json_response = await gemini_service.analyze_frame(data)
            
            try:

                # converts json string to dictionary
                parsed = json.loads(json_response)
                
                command = parsed.get("command","WAIT")
                
                # sends Gemini response to client
                await websocket.send_text(command)

            except json.JSONDecodeError:
                
                logger.warning(f"Failed to parse Gemini output: {json_response}")

    except WebSocketDisconnect:

        logger.warning("Client disconnected")
 