import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

LANGUAGE_NAMES = {
    'en': 'English',
    'hi': 'Hindi',
    'mr': 'Marathi',
    'ml': 'Malayalam',
    'ta': 'Tamil',
    'te': 'Telugu'
}

def translate_text(text: str, from_lang: str, to_lang: str) -> dict:
    if from_lang == to_lang:
        return {
            'success': True,
            'translated': text,
            'from': from_lang,
            'to': to_lang,
            'error': ''
        }

    from_name = LANGUAGE_NAMES.get(from_lang, from_lang)
    to_name   = LANGUAGE_NAMES.get(to_lang, to_lang)

    prompt = (
        f"Translate the following text from {from_name} to {to_name}. "
        f"Reply with ONLY the translated text, nothing else.\n\n"
        f"Text: {text}"
    )

    try:
        response = requests.post(OLLAMA_URL, json={
            "model": "tinyllama",
            "prompt": prompt,
            "stream": False
        }, timeout=30)

        result = response.json()
        translated = result.get('response', '').strip()

        return {
            'success': True,
            'translated': translated,
            'from': from_lang,
            'to': to_lang,
            'error': ''
        }

    except Exception as e:
        return {
            'success': False,
            'translated': text,
            'from': from_lang,
            'to': to_lang,
            'error': str(e)
        }


def translate_emergency_response(response_text: str, target_lang: str) -> str:
    if target_lang == 'en':
        return response_text
    result = translate_text(response_text, 'en', target_lang)
    return result['translated']


def get_installed_languages() -> list:
    return [
        {'code': 'en', 'name': 'English'},
        {'code': 'hi', 'name': 'Hindi'},
        {'code': 'mr', 'name': 'Marathi'},
        {'code': 'ml', 'name': 'Malayalam'},
        {'code': 'ta', 'name': 'Tamil'},
        {'code': 'te', 'name': 'Telugu'},
    ]