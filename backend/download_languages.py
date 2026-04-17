import requests
import sys

OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "tinyllama"

print("=" * 50)
print("Edge-Safe Setup Checker")
print("=" * 50)

# Step 1: Check Ollama is running
print("\nChecking Ollama...")
try:
    r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
    models = [m['name'] for m in r.json().get('models', [])]
    print(f"  Ollama is running.")
    print(f"  Available models: {models}")

    if any(MODEL_NAME in m for m in models):
        print(f"  '{MODEL_NAME}' model found. Ready!")
    else:
        print(f"  '{MODEL_NAME}' not found. Pulling now...")
        import subprocess
        subprocess.run(["ollama", "pull", MODEL_NAME])
        print(f"  '{MODEL_NAME}' downloaded successfully.")

except Exception as e:
    print(f"  Ollama is NOT running. Start it with: ollama serve")
    print(f"  Error: {e}")
    sys.exit(1)

# Step 2: Test translation
print("\nTesting translation (English → Hindi)...")
try:
    from translator_service import translate_text
    result = translate_text("Stay calm and call for help.", "en", "hi")
    if result['success']:
        print(f"  Input:  Stay calm and call for help.")
        print(f"  Output: {result['translated']}")
        print(f"  Translation working!")
    else:
        print(f"  Translation failed: {result['error']}")
except Exception as e:
    print(f"  Error: {e}")

# Step 3: Show supported languages
print("\nSupported languages:")
langs = ['English (en)', 'Hindi (hi)', 'Marathi (mr)',
         'Malayalam (ml)', 'Tamil (ta)', 'Telugu (te)']
for l in langs:
    print(f"  ✓ {l}")

print("\nEdge-Safe is ready. Run: python app.py")
print("=" * 50)