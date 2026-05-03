import requests

OLLAMA_URL = 'http://localhost:11434/api/generate'

LANGUAGE_NAMES = {
    'en': 'English',
    'hi': 'Hindi',
    'mr': 'Marathi',
    'ml': 'Malayalam',
    'ta': 'Tamil',
    'te': 'Telugu',
    'kn': 'Kannada',
}

# ─────────────────────────────────────────────────────
# HARDCODED EMERGENCY TRANSLATIONS
# These are 100% accurate and instant — no AI needed
# ─────────────────────────────────────────────────────
EMERGENCY_DB = {

    # ── HINDI ──
    'hi': {
        # First aid conditions
        'choking':               'दम घुटना',
        'bleeding':              'खून बहना',
        'burn':                  'जलना',
        'fracture':              'हड्डी टूटना',
        'heart attack':          'दिल का दौरा',
        'drowning':              'डूबना',
        'snake bite':            'सांप का काटना',
        'unconscious':           'बेहोशी',
        'electric shock':        'बिजली का झटका',
        'heat stroke':           'लू लगना',
        # Common emergency phrases
        'Stay calm':             'शांत रहें',
        'Call for help':         'मदद के लिए बुलाएं',
        'Apply pressure':        'दबाव डालें',
        'Do not move':           'न हिलें',
        'Go to hospital':        'अस्पताल जाएं',
        'Call emergency':        'आपातकालीन सेवा बुलाएं',
        'Seek medical help':     'चिकित्सा सहायता लें',
        'Move to higher ground': 'ऊंची जगह पर जाएं',
        'Evacuate immediately':  'तुरंत निकलें',
        'Do not panic':          'घबराएं नहीं',
        # Disaster modes
        'flood':                 'बाढ़',
        'fire':                  'आग',
        'earthquake':            'भूकंप',
        'medical':               'चिकित्सा',
        'general':               'सामान्य',
        # Step prefixes
        '1.': '1.',  '2.': '2.',  '3.': '3.',
        '4.': '4.',  '5.': '5.',  '6.': '6.',
        '7.': '7.',  '8.': '8.',
    },

    # ── MARATHI ──
    'mr': {
        'choking':               'श्वास कोंडणे',
        'bleeding':              'रक्तस्त्राव',
        'burn':                  'जळणे',
        'fracture':              'हाड मोडणे',
        'heart attack':          'हृदयविकाराचा झटका',
        'drowning':              'बुडणे',
        'snake bite':            'सापाचा दंश',
        'unconscious':           'बेशुद्धी',
        'electric shock':        'विद्युत धक्का',
        'heat stroke':           'उष्माघात',
        'Stay calm':             'शांत राहा',
        'Call for help':         'मदतीसाठी हाक द्या',
        'Apply pressure':        'दाब द्या',
        'Do not move':           'हलू नका',
        'Go to hospital':        'रुग्णालयात जा',
        'Call emergency':        'आपत्कालीन सेवा बोलवा',
        'Seek medical help':     'वैद्यकीय मदत घ्या',
        'Move to higher ground': 'उंच जागी जा',
        'Evacuate immediately':  'त्वरित बाहेर पडा',
        'Do not panic':          'घाबरू नका',
        'flood':                 'पूर',
        'fire':                  'आग',
        'earthquake':            'भूकंप',
        'medical':               'वैद्यकीय',
        'general':               'सामान्य',
    },

    # ── MALAYALAM ──
    'ml': {
        'choking':               'ശ്വാസം മുട്ടൽ',
        'bleeding':              'രക്തസ്രാവം',
        'burn':                  'പൊള്ളൽ',
        'fracture':              'എല്ല് ഒടിയൽ',
        'heart attack':          'ഹൃദയാഘാതം',
        'drowning':              'മുങ്ങൽ',
        'snake bite':            'പാമ്പ് കടി',
        'unconscious':           'അബോധാവസ്ഥ',
        'electric shock':        'വൈദ്യുതി ആഘാതം',
        'heat stroke':           'ചൂട് സ്ട്രോക്ക്',
        'Stay calm':             'ശാന്തമായിരിക്കുക',
        'Call for help':         'സഹായത്തിനായി വിളിക്കുക',
        'Apply pressure':        'സമ്മർദ്ദം ചെലുത്തുക',
        'Do not move':           'അനങ്ങരുത്',
        'Go to hospital':        'ആശുപത്രിയിൽ പോകുക',
        'Call emergency':        'അടിയന്തര സേവനം വിളിക്കുക',
        'Seek medical help':     'വൈദ്യസഹായം തേടുക',
        'Move to higher ground': 'ഉയർന്ന സ്ഥലത്തേക്ക് പോകുക',
        'Evacuate immediately':  'ഉടൻ ഒഴിഞ്ഞുപോകുക',
        'Do not panic':          'പരിഭ്രമിക്കരുത്',
        'flood':                 'വെള്ളപ്പൊക്കം',
        'fire':                  'തീ',
        'earthquake':            'ഭൂകമ്പം',
        'medical':               'വൈദ്യ',
        'general':               'പൊതു',
    },

    # ── TAMIL ──
    'ta': {
        'choking':               'மூச்சுத் திணறல்',
        'bleeding':              'இரத்தப்போக்கு',
        'burn':                  'தீக்காயம்',
        'fracture':              'எலும்பு முறிவு',
        'heart attack':          'மாரடைப்பு',
        'drowning':              'மூழ்குதல்',
        'snake bite':            'பாம்பு கடி',
        'unconscious':           'மயக்கம்',
        'electric shock':        'மின்சார அதிர்ச்சி',
        'heat stroke':           'வெப்ப அதிர்ச்சி',
        'Stay calm':             'அமைதியாக இருங்கள்',
        'Call for help':         'உதவிக்கு அழையுங்கள்',
        'Apply pressure':        'அழுத்தம் கொடுங்கள்',
        'Do not move':           'அசையாதீர்கள்',
        'Go to hospital':        'மருத்துவமனை செல்லுங்கள்',
        'Call emergency':        'அவசர சேவையை அழையுங்கள்',
        'Seek medical help':     'மருத்துவ உதவி பெறுங்கள்',
        'Move to higher ground': 'உயரமான இடத்திற்கு செல்லுங்கள்',
        'Evacuate immediately':  'உடனே வெளியேறுங்கள்',
        'Do not panic':          'பதட்டப்படாதீர்கள்',
        'flood':                 'வெள்ளம்',
        'fire':                  'தீ',
        'earthquake':            'நிலநடுக்கம்',
        'medical':               'மருத்துவம்',
        'general':               'பொது',
    },

    # ── TELUGU ──
    'te': {
        'choking':               'శ్వాస ఆగిపోవడం',
        'bleeding':              'రక్తస్రావం',
        'burn':                  'కాలిన గాయం',
        'fracture':              'ఎముక విరుపు',
        'heart attack':          'గుండెపోటు',
        'drowning':              'మునిగిపోవడం',
        'snake bite':            'పాము కాటు',
        'unconscious':           'స్పృహ తప్పడం',
        'electric shock':        'విద్యుత్ షాక్',
        'heat stroke':           'వేడి దెబ్బ',
        'Stay calm':             'ప్రశాంతంగా ఉండండి',
        'Call for help':         'సహాయం కోసం పిలవండి',
        'Apply pressure':        'ఒత్తిడి వేయండి',
        'Do not move':           'కదలకండి',
        'Go to hospital':        'ఆసుపత్రికి వెళ్ళండి',
        'Call emergency':        'అత్యవసర సేవలను పిలవండి',
        'Seek medical help':     'వైద్య సహాయం తీసుకోండి',
        'Move to higher ground': 'ఎత్తైన ప్రదేశానికి వెళ్ళండి',
        'Evacuate immediately':  'వెంటనే తరలిపోండి',
        'Do not panic':          'భయపడకండి',
        'flood':                 'వరద',
        'fire':                  'అగ్ని',
        'earthquake':            'భూకంపం',
        'medical':               'వైద్య',
        'general':               'సాధారణ',
    },

    # ── KANNADA ──
    'kn': {
        'choking':               'ಉಸಿರುಗಟ್ಟುವಿಕೆ',
        'bleeding':              'ರಕ್ತಸ್ರಾವ',
        'burn':                  'ಸುಟ್ಟ ಗಾಯ',
        'fracture':              'ಮೂಳೆ ಮುರಿತ',
        'heart attack':          'ಹೃದಯಾಘಾತ',
        'drowning':              'ಮುಳುಗುವಿಕೆ',
        'snake bite':            'ಹಾವು ಕಡಿತ',
        'unconscious':           'ಪ್ರಜ್ಞಾಹೀನ',
        'electric shock':        'ವಿದ್ಯುತ್ ಆಘಾತ',
        'heat stroke':           'ಶಾಖಾಘಾತ',
        'Stay calm':             'ಶಾಂತವಾಗಿರಿ',
        'Call for help':         'ಸಹಾಯಕ್ಕಾಗಿ ಕರೆಯಿರಿ',
        'Apply pressure':        'ಒತ್ತಡ ಹಾಕಿ',
        'Do not move':           'ಅಲುಗಾಡಬೇಡಿ',
        'Go to hospital':        'ಆಸ್ಪತ್ರೆಗೆ ಹೋಗಿ',
        'Call emergency':        'ತುರ್ತು ಸೇವೆ ಕರೆಯಿರಿ',
        'Seek medical help':     'ವೈದ್ಯಕೀಯ ಸಹಾಯ ಪಡೆಯಿರಿ',
        'Move to higher ground': 'ಎತ್ತರದ ಸ್ಥಳಕ್ಕೆ ಹೋಗಿ',
        'Evacuate immediately':  'ತಕ್ಷಣ ಸ್ಥಳಾಂತರಗೊಳ್ಳಿ',
        'Do not panic':          'ಗಾಬರಿಪಡಬೇಡಿ',
        'flood':                 'ಪ್ರವಾಹ',
        'fire':                  'ಬೆಂಕಿ',
        'earthquake':            'ಭೂಕಂಪ',
        'medical':               'ವೈದ್ಯಕೀಯ',
        'general':               'ಸಾಮಾನ್ಯ',
    },
}

# ─────────────────────────────────────────────────────
# SMART TRANSLATION FUNCTION
# Step 1: Check hardcoded DB first (instant + accurate)
# Step 2: Fall back to Ollama only if not found
# ─────────────────────────────────────────────────────
def translate_text(text: str, from_lang: str, to_lang: str) -> dict:
    if from_lang == to_lang:
        return {
            'success':    True,
            'translated': text,
            'from':       from_lang,
            'to':         to_lang,
            'source':     'passthrough',
            'error':      ''
        }

    # ── Step 1: Check hardcoded dictionary first ──
    lang_dict = EMERGENCY_DB.get(to_lang, {})
    if lang_dict:
        if text in lang_dict:
            return {
                'success':    True,
                'translated': lang_dict[text],
                'from':       from_lang,
                'to':         to_lang,
                'source':     'hardcoded',
                'error':      ''
            }

        translated = text
        for eng_phrase, native_phrase in lang_dict.items():
            translated = translated.replace(eng_phrase, native_phrase)

        if translated != text:
            return {
                'success':    True,
                'translated': translated,
                'from':       from_lang,
                'to':         to_lang,
                'source':     'hardcoded_partial',
                'error':      ''
            }

    # ── Step 2: Fall back to Ollama AI ──       ← ADD NEW PROMPT HERE
    from_name = LANGUAGE_NAMES.get(from_lang, from_lang)
    to_name   = LANGUAGE_NAMES.get(to_lang,   to_lang)

    prompt = (
        f"Translate to {to_name} only.\n"
        f"Input: {text}\n"
        f"Output only the {to_name} translation, nothing else:"
    )

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                'model':  'tinyllama',
                'prompt': prompt,
                'stream': False,
                'options': {'temperature': 0.1, 'num_predict': 200}
            },
            timeout=30
        )
        result     = response.json()
        translated = result.get('response', '').strip()

        if len(translated) > len(text) * 4:
            translated = text

        return {
            'success':    True,
            'translated': translated,
            'from':       from_lang,
            'to':         to_lang,
            'source':     'ollama',
            'error':      ''
        }

    except Exception as e:
        return {
            'success':    False,
            'translated': text,
            'from':       from_lang,
            'to':         to_lang,
            'source':     'fallback',
            'error':      str(e)
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
        {'code': 'kn', 'name': 'Kannada'},
    ]