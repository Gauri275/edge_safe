import requests

OLLAMA_BASE_URL = 'http://localhost:11434'
MODEL_NAME = 'tinyllama'

SYSTEM_PROMPTS = {
    'medical': (
        "You are an offline first-aid assistant for emergencies. "
        "Give clear, numbered step-by-step instructions. "
        "Be concise and direct. "
        "Always end with: 'Seek medical help as soon as possible.'"
    ),
    'flood': (
        "You are an emergency assistant during a flood disaster. "
        "Give short, numbered evacuation and safety steps. "
        "Focus on immediate actions to stay safe."
    ),
    'fire': (
        "You are an emergency assistant during a fire emergency. "
        "Give clear numbered steps to escape safely. "
        "Mention smoke avoidance and not using elevators."
    ),
    'earthquake': (
        "You are an emergency assistant during an earthquake. "
        "Give Drop-Cover-Hold instructions and post-quake safety steps."
    ),
    'general': (
        "You are an offline emergency assistant. "
        "Give concise, numbered, life-saving guidance for any emergency situation."
    ),
}

def check_ollama_running() -> bool:
    try:
        response = requests.get(f'{OLLAMA_BASE_URL}/api/tags', timeout=3)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False

def get_ai_response(query: str, mode: str = 'general') -> dict:
    if not check_ollama_running():
        return {
            'success': False,
            'answer': '',
            'error': 'Ollama is not running. Please start it with: ollama serve'
        }

    system_prompt = SYSTEM_PROMPTS.get(mode, SYSTEM_PROMPTS['general'])
    full_prompt = f"{system_prompt}\n\nUser emergency query: {query}\n\nResponse:"

    payload = {
        'model': MODEL_NAME,
        'prompt': full_prompt,
        'stream': False,
        'options': {
            'temperature': 0.3,
            'num_predict': 300,
        }
    }

    try:
        response = requests.post(
            f'{OLLAMA_BASE_URL}/api/generate',
            json=payload,
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            return {
                'success': True,
                'answer': data.get('response', '').strip(),
                'error': ''
            }
        else:
            return {
                'success': False,
                'answer': '',
                'error': f'Ollama returned error: {response.status_code}'
            }
    except requests.exceptions.Timeout:
        return {
            'success': False,
            'answer': '',
            'error': 'AI model timed out. Try a simpler query or restart Ollama.'
        }
    except Exception as e:
        return {
            'success': False,
            'answer': '',
            'error': f'Unexpected error: {str(e)}'
        }

def list_available_models() -> list:
    try:
        response = requests.get(f'{OLLAMA_BASE_URL}/api/tags', timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            return [m['name'] for m in models]
        return []
    except:
        return []