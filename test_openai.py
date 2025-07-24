import openai

# Masukkan API key langsung di sini
openai.api_key = "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"

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",  # Bisa diganti "gpt-4o-mini"
    messages=[
        {"role": "system", "content": "Kamu adalah AI asisten yang ramah."},
        {"role": "user", "content": "Hai, siapa namamu?"}
    ]
)

print(response.choices[0].message["content"])
