from translator_service import translate_text

tests = [
    ('Hello, stay calm.', 'en', 'ml'),
    ('Hello, stay calm.', 'en', 'mr'),
    ('Hello, stay calm.', 'en', 'ta'),
    ('Hello, stay calm.', 'en', 'te'),
]

for text, f, t in tests:
    result = translate_text(text, f, t)
    print(f"{f} -> {t}: {result['translated']}")