from openai import OpenAI
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- STEP 1: Load your file ---
with open("context.txt", "r") as f:
    context_text = f.read()

# --- STEP 2: Create embeddings for your file ---
file_embedding = client.embeddings.create(
    model="text-embedding-3-small",
    input=context_text
).data[0].embedding

# --- STEP 3: Ask a question ---
user_query = input("Ask a question: ")

query_embedding = client.embeddings.create(
    model="text-embedding-3-small",
    input=user_query
).data[0].embedding

# --- STEP 4: Compute cosine similarity ---
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

similarity = cosine_similarity(file_embedding, query_embedding)

# --- STEP 5: Send question + context to GPT if relevant ---
if similarity > 0.5:
    context = context_text
else:
    context = ""

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are an AI assistant that answers questions using context from a file when relevant."},
        {"role": "user", "content": f"Question: {user_query}\n\nRelevant context:\n{context}"}
    ]
)

print("\n--- Response ---\n")
print(response.choices[0].message.content)
