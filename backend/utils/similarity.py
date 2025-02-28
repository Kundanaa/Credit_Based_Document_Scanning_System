# utils/similarity.py - Text Similarity Functions
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#import openai  # AI-based similarity (optional)
from sentence_transformers import SentenceTransformer
import os
import asyncio
from sklearn.pipeline import Pipeline
#openai.api_key = os.getenv("OPENAI_API_KEY")

model = SentenceTransformer('all-MiniLM-L6-v2')
tfidf_pipeline = Pipeline([
    ('vectorizer', TfidfVectorizer())
])

def compute_tfidf_similarity(new_doc, stored_docs):
    """
    Compute text similarity using TF-IDF & cosine similarity.
    """
    try:
        documents = [new_doc] + stored_docs
        vectors = tfidf_pipeline.fit_transform(documents).toarray()
        return cosine_similarity([vectors[0]], vectors[1:])[0]
    except Exception as e:
        print("TF-IDF Similarity Error:", str(e))
        return []

def get_openai_embedding(text):
    """
    Get OpenAI embedding for a given text.
    """
    try:
        response = openai.embeddings.create(
            model="text-embedding-ada-002",  
            input=text
        )
        return response.data[0].embedding  # Extract embedding vector
    except Exception as e:
        print("Embedding API error:", str(e))
        return None  # Return None if embedding fails

def get_embedding(text):
    """
    Get sentence embedding using Sentence-Transformers.
    """
    try:
        embedding = model.encode([text])[0]  # Extract embedding vector
        return np.array(embedding, dtype=np.float32)  # Ensure it's an array
    except Exception as e:
        print("Embedding Error:", str(e))
        return None  # Return None if embedding fails

async def async_get_embedding(text):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, get_embedding, text)


# async def async_get_openai_embedding(text):
#     # response = await openai.embeddings.create(model="text-embedding-ada-002", input=text)
#     # return response.data[0].embedding
#     loop = asyncio.get_event_loop()
#     return await loop.run_in_executor(None, get_openai_embedding, text)

async def compute_ai_similarity(new_doc, stored_docs):
    """
    Compute document similarity using OpenAI embeddings.
    """
    epsilon = 1e-9  # Small value to prevent division by zero
    new_embedding = await async_get_embedding(new_doc)
    # Ensure new_embedding is a NumPy array
    # Debugging: Check new_embedding
    print(f"✅ Debug: new_embedding type={type(new_embedding)}, shape={getattr(new_embedding, 'shape', None)}")

    if new_embedding is None:
        print("❌ Error: Failed to get embedding for new_doc")
        return []
    
    new_embedding = np.array(new_embedding, dtype=np.float32)
    stored_embeddings = await asyncio.gather(*(async_get_embedding(doc) for doc in stored_docs))
    print(f"✅ Debug: Before filtering stored_embeddings -> {type(stored_embeddings)}, length={len(stored_embeddings)}")
    
    stored_embeddings = [np.array(emb, dtype=np.float32) for emb in stored_embeddings if emb is not None] # Filter out failed embeddings

    if not stored_embeddings or new_embedding is None:
        print("❌ Error: No valid embeddings found for stored_docs")
        return []  # Return empty if no valid embeddings exist
    
    # Compute similarity
    similarities = []
    for emb in stored_embeddings:
        if emb.shape != new_embedding.shape:
            print(f"❌ Error: Shape mismatch between new_embedding ({new_embedding.shape}) and stored embedding ({emb.shape})")
            continue  # Skip problematic embeddings

        sim = np.dot(new_embedding, emb) / max(np.linalg.norm(new_embedding) * np.linalg.norm(emb), epsilon)
        similarities.append(sim)

    return similarities
