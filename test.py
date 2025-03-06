from google import genai

client = genai.Client(api_key="AIzaSyCfi6HMfYQ6QRaF2S_uP2QhBXOjAYnor7A")
response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents='Tell me a story in 300 words.'
)
print(response.text)

print(response.model_dump_json(
    exclude_none=True, indent=4))