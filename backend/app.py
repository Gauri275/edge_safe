from flask import Flask, request, jsonify
from flask_cors import CORS
from database import search_first_aid, get_shelters, get_evacuation, create_tables
from ai_service import get_ai_response, check_ollama_running, list_available_models
from map_service import generate_shelter_map, generate_evacuation_map, get_map_path
from flask import Flask, request, jsonify, send_file
import json

from translator_service import translate_text, translate_emergency_response, get_installed_languages

app = Flask(__name__)
CORS(app)  # allow Flutter app to make requests from any origin
app.config['JSON_AS_ASCII'] = False  # ← ADD THIS LINE
app.json.ensure_ascii = False   # Flask 2.x way

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'app': 'Edge-Safe Emergency Assistant',
        'status': 'running',
        'version': '1.0',
        'routes': {
            'GET  /health':                    'Check server and Ollama status',
            'GET  /firstaid?q=&lang=':         'Search first aid by condition',
            'GET  /shelters?city=':            'Get nearby shelters',
            'GET  /evacuation?type=&lang=':    'Get evacuation instructions',
            'POST /ask':                       'Main emergency query (DB + AI)',
            'POST /ai':                        'Direct AI query only'
        }
    })
# ─────────────────────────────────────────────────────
# ROUTE 1: Health check
# GET /health
# Returns server status and Ollama status
# ─────────────────────────────────────────────────────
@app.route('/health', methods=['GET'])
def health():
    ollama_ok = check_ollama_running()
    models    = list_available_models() if ollama_ok else []
    return jsonify({
        'status':        'running',
        'ollama_online': ollama_ok,
        'models':        models
    })

# ─────────────────────────────────────────────────────
# ROUTE 2: First aid lookup (from SQLite DB)
# GET /firstaid?q=choking&lang=en
# ─────────────────────────────────────────────────────
@app.route('/firstaid', methods=['GET'])
def first_aid():
    query    = request.args.get('q', '').strip()
    language = request.args.get('lang', 'en').strip()

    if not query:
        return jsonify({'error': 'Query parameter q is required'}), 400

    results = search_first_aid(query, language)

    if results:
        return jsonify({
            'source':  'database',
            'found':   True,
            'results': results
        })
    else:
        return jsonify({
            'source':  'database',
            'found':   False,
            'results': []
        })

# ─────────────────────────────────────────────────────
# ROUTE 3: Get nearby shelters
# GET /shelters?city=Solapur
# ─────────────────────────────────────────────────────
@app.route('/shelters', methods=['GET'])
def shelters():
    city    = request.args.get('city', '').strip()
    results = get_shelters(city)
    return jsonify({'shelters': results, 'count': len(results)})

# ─────────────────────────────────────────────────────
# ROUTE 4: Evacuation instructions
# GET /evacuation?type=flood&lang=en
# ─────────────────────────────────────────────────────
@app.route('/evacuation', methods=['GET'])
def evacuation():
    disaster_type = request.args.get('type', 'flood').strip()
    language      = request.args.get('lang', 'en').strip()
    results       = get_evacuation(disaster_type, 'en')

    if language != 'en':
        try:
            for item in results:
                translated = translate_text(item['instructions'], 'en', language)
                if translated['success']:
                    item['instructions'] = translated['translated']
        except Exception:
            pass  # Return English if translation fails


    return jsonify({'instructions': results, 'count': len(results)})

# ─────────────────────────────────────────────────────
# ROUTE 5: Main emergency query (DB first, then AI)
# POST /ask
# Body: { "query": "...", "mode": "medical", "lang": "en", "city": "Solapur" }
# ─────────────────────────────────────────────────────
@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    
    if not data or 'query' not in data:

        return jsonify({'error': 'query field is required'}), 400

    query    = data.get('query', '').strip()
    mode     = data.get('mode', 'general')
    language = data.get('lang', 'en')

    city     = data.get('city', 'Solapur')

    result = {
        'query':      query,
        'mode':       mode,
        'answer':     '',
        'source':     '',        # 'database' or 'ai_model'
        'confidence': '',        # 'high' or 'medium'

        'shelters':   [],
        'evacuation': []
    }


    # ── Step 1: Search SQLite DB first ──
    db_results = search_first_aid(query, language)
    if db_results:
        result['answer']     = db_results[0]['steps']
        result['source']     = 'database'

        result['confidence'] = 'high'   # verified data


    # ── Step 2: Disaster mode extras ──
    if mode in ['flood', 'fire', 'earthquake']:
        evac = get_evacuation(mode, language)
        if evac:
            result['evacuation'] = evac
            if not result['answer']:
                result['answer']     = evac[0]['instructions']
                result['source']     = 'database'
                result['confidence'] = 'high'

        result['shelters'] = get_shelters(city)

    # ── Step 3: Not in DB — ask Ollama AI ──
    # This handles ANY question the user asks, even outside the DB

    if not result['answer']:
        ai_result = get_ai_response(query, mode)
        if ai_result['success']:
            result['answer']     = ai_result['answer']
            result['source']     = 'ai_model'

            result['confidence'] = 'medium'  # AI-generated, not verified
        else:
            result['answer'] = (
                'Could not get a response.\n\n'
                'Please make sure:\n'
                '1. Ollama is running: ollama serve\n'

                f'2. Error: {ai_result["error"]}'
            )
            result['source']     = 'error'

            result['confidence'] = 'none'


    return jsonify(result)

# ─────────────────────────────────────────────────────
# ROUTE 6: Direct AI query (bypass DB)
# POST /ai
# Body: { "query": "...", "mode": "general" }
# ─────────────────────────────────────────────────────
@app.route('/ai', methods=['POST'])
def ai_only():
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({'error': 'query field required'}), 400

    query  = data.get('query', '')
    mode   = data.get('mode', 'general')

    if not check_ollama_running():
        return jsonify({
            'success': False,
            'answer': 'AI assistant is offline. Start Ollama with: ollama serve',
            'source': 'offline'
        })


    result = get_ai_response(query, mode)
    return jsonify(result)


# ─────────────────────────────────────────────────────
# ROUTE 7: Generate offline shelter map
# GET /map?type=flood&city=Solapur
# ─────────────────────────────────────────────────────
@app.route('/map', methods=['GET'])
def get_map():
    disaster_type = request.args.get('type', 'general')
    city          = request.args.get('city', 'Solapur')

    # Get shelters from DB
    shelters = get_shelters(city)

    if not shelters:
        return jsonify({'error': 'No shelters found for this city'}), 404

    # Generate the map HTML
    map_path = generate_shelter_map(shelters, disaster_type)

    if map_path:
        # Return the HTML file directly — Flutter will open it in WebView
        from flask import send_file
        return send_file(map_path, mimetype='text/html')

    return jsonify({'error': 'Could not generate map'}), 500


# ─────────────────────────────────────────────────────
# ROUTE 8: Generate evacuation route map
# GET /evacmap?type=flood&city=Solapur&lat=17.68&lng=75.90
# ─────────────────────────────────────────────────────
@app.route('/evacmap', methods=['GET'])
def get_evac_map():
    disaster_type = request.args.get('type', 'flood')
    city          = request.args.get('city', 'Solapur')
    user_lat      = float(request.args.get('lat', 17.6805))
    user_lng      = float(request.args.get('lng', 75.9064))

    shelters = get_shelters(city)

    if not shelters:
        return jsonify({'error': 'No shelters found'}), 404

    map_path = generate_evacuation_map(shelters, disaster_type, user_lat, user_lng)

    if map_path:
        from flask import send_file
        return send_file(map_path, mimetype='text/html')

    return jsonify({'error': 'Could not generate evacuation map'}), 500


# ─────────────────────────────────────────────────────
# ROUTE 9: Translate any text offline
# POST /translate
# Body: { "text": "...", "from": "en", "to": "hi" }
# ─────────────────────────────────────────────────────
@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({'error': 'text field is required'}), 400

    text      = data.get('text', '')
    from_lang = data.get('from', 'en')
    to_lang   = data.get('to', 'hi')

    if not check_ollama_running():
        return jsonify({
            'success': False,
            'translated': text,
            'from': from_lang,
            'to': to_lang,
            'error': 'Translation offline. Start Ollama with: ollama serve'
        })

    result = translate_text(text, from_lang, to_lang)
    return jsonify(result)


# ─────────────────────────────────────────────────────
# ROUTE 10: Auto-translate emergency response
# POST /ask_translated
# Body: { "query": "...", "mode": "...", "lang": "hi" }
# Same as /ask but auto-translates response to target lang
# ─────────────────────────────────────────────────────
@app.route('/ask_translated', methods=['POST'])
def ask_translated():
    data = request.get_json()

    if not data or 'query' not in data:
        return jsonify({'error': 'query field is required'}), 400

    query    = data.get('query', '').strip()
    mode     = data.get('mode', 'general')
    lang     = data.get('lang', 'en')
    city     = data.get('city', 'Solapur')
    
    ollama_online = check_ollama_running()

      # Step 1: If query is in Hindi/Marathi, translate to English first
    query_in_english = query
    if lang != 'en' and ollama_online:
        translated_query = translate_text(query, lang, 'en')
        if translated_query['success']:
            query_in_english = translated_query['translated']
    # Step 2: Get emergency response (always in English from DB/AI)
    from database import search_first_aid, get_shelters, get_evacuation
    from ai_service import get_ai_response

    answer = ''
    source = ''

    db_results = search_first_aid(query_in_english, 'en')
    if db_results:
        answer = db_results[0]['steps']
        source = 'database'
    else:
        ai_result = get_ai_response(query_in_english, mode)
        if ai_result['success']:
            answer = ai_result['answer']
            source = 'ai_model'

   # Step 3: Translate response to requested language
    translated_answer = answer
    if lang != 'en' and answer and ollama_online:
        translated_answer = translate_emergency_response(answer, lang)
        
    shelters = get_shelters(city) if mode in ['flood', 'fire', 'earthquake'] else []

    return jsonify({
        'query':              query,
        'query_in_english':   query_in_english,
        'answer':             translated_answer,
        'answer_in_english':  answer,
        'source':             source,
        'lang':               lang,
        'shelters':           shelters
    })


# ─────────────────────────────────────────────────────
# ROUTE 11: List installed translation languages
# GET /languages
# ─────────────────────────────────────────────────────
@app.route('/languages', methods=['GET'])
def languages():
    return jsonify({'installed_pairs': get_installed_languages()})




# ─────────────────────────────────────────────────────
# START SERVER
# ─────────────────────────────────────────────────────
if __name__ == '__main__':
    print("Initializing database...")
    create_tables()
    print("Starting Edge-Safe backend on http://localhost:5001")
    print("Available routes:")
    print("  GET  /health")
    print("  GET  /firstaid?q=choking&lang=en")
    print("  GET  /shelters?city=Solapur")
    print("  GET  /evacuation?type=flood&lang=en")
    print("  POST /ask   { query, mode, lang, city }")
    print("  POST /ai    { query, mode }")
    app.run(host='0.0.0.0', port=5001, debug=True)
