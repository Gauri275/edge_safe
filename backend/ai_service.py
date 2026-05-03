import requests

OLLAMA_BASE_URL = 'http://localhost:11434'
MODEL_NAME      = 'tinyllama'

# Much more detailed system prompt — covers any emergency question
MASTER_PROMPT = """You are Edge-Safe, an offline emergency assistant deployed in disaster zones.
You have expert knowledge in:
- First aid and medical emergencies
- Natural disasters: floods, earthquakes, cyclones, fires, landslides, tsunamis
- Chemical/gas leaks and industrial accidents
- Search and rescue basics
- Survival techniques without resources
- Emergency communication and signaling
- Food and water safety during disasters
- Psychological first aid for trauma victims

Rules you must always follow:
1. Always give numbered step-by-step instructions
2. Be concise — maximum 8 steps
3. Start with the most critical action first
4. If the situation is life-threatening, say so clearly
5. End every medical response with: "Get professional help as soon as possible."
6. Never give medication dosages — only general guidance
7. If you don't know, say "I am not certain — please seek expert help"

The user may be in an active emergency. Be calm, clear, and direct."""

MODE_EXTRAS = {
    'medical':    "Focus on first aid. The person may be injured right now.",
    'flood':      "The user may be in or near floodwater. Prioritize immediate safety.",
    'fire':       "Assume there may be smoke and flames nearby. Prioritize escape.",
    'earthquake': "Assume the earthquake may still be occurring or just ended.",
    'general':    "Answer the emergency question as clearly as possible.",
}

def check_ollama_running() -> bool:
    try:
        r = requests.get(f'{OLLAMA_BASE_URL}/api/tags', timeout=3)
        return r.status_code == 200
    except:
        return False

def get_ai_response(query: str, mode: str = 'general') -> dict:
    if not check_ollama_running():
        return {
            'success': False,
            'answer':  '',
            'error':   'Ollama not running. Start with: ollama serve'
        }

    # Simple short prompt — tinyllama works better with short prompts
    prompt = f"First aid steps for: {query}\nGive 5 numbered steps only:"

    payload = {
        'model':   MODEL_NAME,
        'prompt':  prompt,
        'stream':  False,
        'options': {
            'temperature': 0.1,
            'num_predict': 250,
            'stop': ['\n\n\n', 'User:', 'Context:', 'Rules:']
        }
    }

    try:
        response = requests.post(
            f'{OLLAMA_BASE_URL}/api/generate',
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            data   = response.json()
            answer = data.get('response', '').strip()

            # Clean up prompt leakage — remove if tinyllama repeats instructions
            cutoff_phrases = [
                'Context:', 'Rules:', 'Note:', 'Edge-Safe:',
                'Be calm', 'User:', 'Assistant:', 'Translate',
                'Sure! Here', 'Here is', 'Here are'
            ]
            for phrase in cutoff_phrases:
                if phrase in answer:
                    answer = answer[:answer.index(phrase)].strip()

            # If answer is too short after cleanup use fallback message
            if len(answer) < 20:
                answer = (
                    'Please follow these general steps:\n'
                    '1. Stay calm and assess the situation.\n'
                    '2. Call emergency services if available.\n'
                    '3. Keep the person still and comfortable.\n'
                    '4. Do not give food or water.\n'
                    '5. Wait for professional help to arrive.'
                )

            return {
                'success': True,
                'answer':  answer,
                'error':   ''
            }

        return {
            'success': False,
            'answer':  '',
            'error':   f'Ollama error: {response.status_code}'
        }

    except requests.exceptions.Timeout:
        return {
            'success': False,
            'answer':  '',
            'error':   'AI timed out. Try restarting Ollama.'
        }
    except Exception as e:
        return {
            'success': False,
            'answer':  '',
            'error':   str(e)
        }

def list_available_models() -> list:
    try:
        r = requests.get(f'{OLLAMA_BASE_URL}/api/tags', timeout=5)
        if r.status_code == 200:
            return [m['name'] for m in r.json().get('models', [])]
        return []
    except:
        return []