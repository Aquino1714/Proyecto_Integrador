import test_ollama

# Llamamos al modelo que configuraste en tu archivo local
response = test_ollama.chat(
    model='qwen2.5-coder:3b', 
    messages=[
        {
            'role': 'user',
            'content': 'Escribe un script básico de Python que salude al usuario.',
        },
    ]
)

print(response['message']['content'])