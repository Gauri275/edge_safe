from flask import Flask, request, jsonify
from flask_cors import CORS
from database import search_first_aid, get_shelters, get_evacuation, create_tables
from ai_service import get_ai_response, check_ollama_running, list_available_models

app = Flask(__name__)
CORS(app)  # allow Flutter app to make requests from any origin


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
    results       = get_evacuation(disaster_type, language)
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
        return jsonify({'error': 'JSON body with query field is required'}), 400

    query    = data.get('query', '').strip()
    mode     = data.get('mode', 'general').strip()
    language = data.get('lang', 'en').strip()
    city     = data.get('city', 'Solapur').strip()

    response_data = {
        'query':     query,
        'mode':      mode,
        'answer':    '',
        'source':    '',
        'shelters':  [],
        'evacuation': []
    }

    # ── Step 1: Search SQLite database first (fastest, no AI needed) ──
    db_results = search_first_aid(query, language)
    if db_results:
        response_data['answer']  = db_results[0]['steps']
        response_data['source']  = 'database'

    # ── Step 2: Add evacuation info for disaster modes ──
    if mode in ['flood', 'fire', 'earthquake']:
        evac = get_evacuation(mode, language)
        if evac:
            response_data['evacuation'] = evac
            if not response_data['answer']:
                response_data['answer'] = evac[0]['instructions']
                response_data['source'] = 'database'

        # Also attach nearby shelters
        shelter_list = get_shelters(city)
        response_data['shelters'] = shelter_list

    # ── Step 3: If nothing found in DB, use AI model ──
    if not response_data['answer']:
        ai_result = get_ai_response(query, mode)
        if ai_result['success']:
            response_data['answer'] = ai_result['answer']
            response_data['source'] = 'ai_model'
        else:
            response_data['answer'] = (
                'Could not get a response. '
                'Make sure Ollama is running: ollama serve\n\n'
                f'Error: {ai_result["error"]}'
            )
            response_data['source'] = 'error'

    return jsonify(response_data)

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
    result = get_ai_response(query, mode)
    return jsonify(result)

# ─────────────────────────────────────────────────────
# START SERVER
# ─────────────────────────────────────────────────────
if __name__ == '__main__':
    print("Initializing database...")
    create_tables()
    print("Starting Edge-Safe backend on http://localhost:5000")
    print("Available routes:")
    print("  GET  /health")
    print("  GET  /firstaid?q=choking&lang=en")
    print("  GET  /shelters?city=Solapur")
    print("  GET  /evacuation?type=flood&lang=en")
    print("  POST /ask   { query, mode, lang, city }")
    print("  POST /ai    { query, mode }")
    app.run(host='0.0.0.0', port=5000, debug=True)