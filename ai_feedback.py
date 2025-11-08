import os
import requests
import json
import time

# NOTE: This file now requires the API key to be passed as the first argument 
# to all functions, which is handled by app.py.

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent"

# Provider can be 'gemini' (default) or other implementations in future.
AI_PROVIDER = os.environ.get('AI_PROVIDER', 'gemini').lower()

# If AI_MOCK is set (or API key is literally 'MOCK'), return canned responses for local development/tests.
AI_MOCK = os.environ.get('AI_MOCK', '')

def call_gemini_api(api_key, payload):
    """
    Handles the API call to Gemini with a robust, simplified structure.
    """
    headers = {
        'Content-Type': 'application/json'
    }

    # Handle missing API key or mock mode
    if not api_key or api_key == '':
        if AI_MOCK == '1' or api_key == 'MOCK':
            return None  # Let caller use the mock responder
        return "ERROR: AI API key is not set. Set GEMINI_API_KEY or use AI_MOCK=1 for local testing."

    # Robust request loop with exponential backoff
    for i in range(3):
        try:
            url = f"{GEMINI_API_URL}?key={api_key}"
            # Use a short timeout to prevent the Flask server from hanging indefinitely
            response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=15)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

            result = response.json()

            # Extract text content from the deep JSON structure
            if ('candidates' in result and result['candidates'] and
                    'content' in result['candidates'][0] and
                    'parts' in result['candidates'][0]['content'] and
                    result['candidates'][0]['content']['parts'] and
                    'text' in result['candidates'][0]['content']['parts'][0]):
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                raise KeyError("Text content not found in Gemini response.")

        except requests.exceptions.RequestException as e:
            # Log specific network/API error, especially the 403 Forbidden error
            print(f"DEBUG: Gemini API Call Failed (Attempt {i+1}): {e}")
            if i < 2:
                time.sleep(2 ** i) # Wait 1s, 2s
                continue
            return "ERROR: AI service unreachable. The connection timed out or was rejected (403). Please check the API key."

        except Exception as e:
            print(f"DEBUG: Unexpected error in Gemini response processing: {e}")
            return "ERROR: Received an unexpected or malformed response from the AI system."

    return "ERROR: AI service failed after multiple retries."


def get_ai_explanation(api_key, error_code, state_info):
    """
    Generates a contextual explanation for a mission failure.
    Requires api_key, error_code, and state_info.
    """
    system_prompt = (
        "You are a friendly, knowledgeable Mission Control AI for middle school students. "
        "Your task is to analyze a mission failure, explain the core physics or engineering "
        "mistake simply and engagingly, and suggest ONE concrete action the student should "
        "take to fix it on the next attempt. Respond concisely in a single paragraph, using simple markdown for formatting."
    )
    
    user_query = (
        f"The mission failed with error code: {error_code}. The state of the vehicle at failure was: "
        f"Fuel Left: {state_info['fuel']:.2f}, Velocity: {state_info['velocity_km_s']:.2f} km/s, "
        f"Altitude: {state_info['altitude_km']:.0f} km. "
        f"Explain the failure simply and tell the student exactly what to change."
    )
    
    payload = {
        "contents": [{"parts": [{"text": user_query}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "tools": [{"google_search": {}}], 
    }
    # If mock/testing mode requested, return a helpful, canned reply
    if AI_MOCK == '1' or api_key == 'MOCK':
        return (
            f"**Mission Failure ({error_code})** — You ran out of necessary resources or applied incorrect inputs. "
            "Try adjusting the mission parameters: increase thrust or ensure more fuel before launch. "
            "On the next attempt, raise the thrust by ~20% or refuel to at least 200 units."
        )

    return call_gemini_api(api_key, payload)


def get_ai_chat_response(api_key, query):
    """
    Generates a general space science chat response.
    Requires api_key and the student's query.
    """
    system_prompt = (
        "You are a supportive Space Science Educator for middle school students. "
        "Answer the student's question concisely, clearly, and enthusiastically. Use simple language."
    )

    payload = {
        "contents": [{"parts": [{"text": query}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "tools": [{"google_search": {}}], 
    }
    # Mock short reply for development/testing
    if AI_MOCK == '1' or api_key == 'MOCK':
        return f"Mock AI Reply: That's a great question about '{query}'. Try exploring the rocket's fuel and thrust trade-offs!"

    return call_gemini_api(api_key, payload)