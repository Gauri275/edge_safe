import requests

BASE = 'http://localhost:5000'

results = []

def test(name, method, url, body=None, check_key=None, check_value=None):
    try:
        if method == 'GET':
            r = requests.get(url, timeout=15)
        else:
            r = requests.post(url, json=body, timeout=30)

        if r.status_code != 200:
            results.append(f'  FAIL  {name} — HTTP {r.status_code}')
            return

        data = r.json() if 'map' not in url else {}

        if check_key and check_value:
            actual = data.get(check_key)
            if actual == check_value:
                results.append(f'  PASS  {name}')
            else:
                results.append(
                    f'  WARN  {name} — '
                    f'expected {check_key}={check_value}, got {actual}'
                )
        else:
            results.append(f'  PASS  {name}')

    except Exception as e:
        results.append(f'  FAIL  {name} — {str(e)}')

print('=' * 55)
print('Edge-Safe Full System Check')
print('=' * 55)

# Backend
test('Health check',          'GET',  f'{BASE}/health',
     check_key='status', check_value='running')
test('Ollama online',         'GET',  f'{BASE}/health',
     check_key='ollama_online', check_value=True)

# Database
test('First aid EN',          'GET',  f'{BASE}/firstaid?q=choking&lang=en')
test('First aid HI',          'GET',  f'{BASE}/firstaid?q=दम&lang=hi')
test('First aid ML',          'GET',  f'{BASE}/firstaid?q=ശ്വാസം&lang=ml')
test('First aid TA',          'GET',  f'{BASE}/firstaid?q=மூச்சு&lang=ta')
test('First aid TE',          'GET',  f'{BASE}/firstaid?q=శ్వాస&lang=te')
test('First aid KN',          'GET',  f'{BASE}/firstaid?q=ಉಸಿರು&lang=kn')
test('Shelters',              'GET',  f'{BASE}/shelters?city=Solapur')
test('Evacuation flood',      'GET',  f'{BASE}/evacuation?type=flood&lang=en')

# Ask routes
test('Ask from DB',           'POST', f'{BASE}/ask',
     body={'query': 'bleeding', 'mode': 'medical',
           'lang': 'en', 'city': 'Solapur'},
     check_key='source', check_value='database')

test('Ask AI fallback',       'POST', f'{BASE}/ask',
     body={'query': 'gas leak in kitchen',
           'mode': 'general', 'lang': 'en', 'city': 'Solapur'})

test('Ask flood mode',        'POST', f'{BASE}/ask',
     body={'query': 'flood', 'mode': 'flood',
           'lang': 'en', 'city': 'Solapur'})

# Translation
test('Translate → Hindi',     'POST', f'{BASE}/translate',
     body={'text': 'choking', 'from': 'en', 'to': 'hi'},
     check_key='success', check_value=True)

test('Translate → Malayalam', 'POST', f'{BASE}/translate',
     body={'text': 'bleeding', 'from': 'en', 'to': 'ml'},
     check_key='success', check_value=True)

test('Translate → Tamil',     'POST', f'{BASE}/translate',
     body={'text': 'Stay calm', 'from': 'en', 'to': 'ta'},
     check_key='success', check_value=True)

test('Translate → Telugu',    'POST', f'{BASE}/translate',
     body={'text': 'Go to hospital', 'from': 'en', 'to': 'te'},
     check_key='success', check_value=True)

test('Translate → Kannada',   'POST', f'{BASE}/translate',
     body={'text': 'Call emergency', 'from': 'en', 'to': 'kn'},
     check_key='success', check_value=True)

test('Translate → Marathi',   'POST', f'{BASE}/translate',
     body={'text': 'Do not panic', 'from': 'en', 'to': 'mr'},
     check_key='success', check_value=True)

# Ask translated
test('Ask translated HI',     'POST', f'{BASE}/ask_translated',
     body={'query': 'choking', 'mode': 'medical',
           'lang': 'hi', 'city': 'Solapur'})

test('Ask translated ML',     'POST', f'{BASE}/ask_translated',
     body={'query': 'bleeding', 'mode': 'medical',
           'lang': 'ml', 'city': 'Solapur'})

test('Ask translated TA',     'POST', f'{BASE}/ask_translated',
     body={'query': 'burn', 'mode': 'medical',
           'lang': 'ta', 'city': 'Solapur'})

test('Ask translated KN',     'POST', f'{BASE}/ask_translated',
     body={'query': 'heart attack', 'mode': 'medical',
           'lang': 'kn', 'city': 'Solapur'})

# Languages
test('Languages list',        'GET',  f'{BASE}/languages')

# Print results
print()
passed = sum(1 for r in results if 'PASS' in r)
failed = sum(1 for r in results if 'FAIL' in r)
warned = sum(1 for r in results if 'WARN' in r)

for r in results:
    print(r)

print()
print('=' * 55)
print(f'PASSED: {passed}  |  WARNED: {warned}  |  FAILED: {failed}')
print('=' * 55)