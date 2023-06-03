"""
Create embeddings for texts using the OpenAI API and store them in Pinecone's Vector Database
Also expose other OpenAI API functionality
"""

import random
import string
from typing import List

import pinecone
import openai
# use a .env file for keys
import dotenv
import os

import logging

# load .env file
dotenv.load_dotenv()

# Authenticate with OpenAI
openai.organization = os.getenv("OPENAI_ORG_ID")
openai.api_key = os.getenv("OPENAI_API_KEY")
# Authenticate with Pinecone
pinecone.init(api_key = os.getenv("PINECONE_API_KEY"), environment = os.getenv("PINECONE_ENVIRONMENT"))

def create_index():
    logging.info('Creating pinecone index')
    pinecone.create_index(name='researcher', dimension=1536, metric='cosine', shards=1)
index = pinecone.Index("researcher")

# create a random 6 letter id for a vector
def generate_id(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def upsert_vectors(vectors, metadata):
    '''Upsert vectors and metadata to the pinecone index'''
    index.upsert([pinecone.Vector(id=generate_id(), values=v, metadata=m) for v, m in zip(vectors, metadata)], show_progress=True)

def embed_texts(texts) -> List[float]:
    '''Embed a list of texts using the OpenAI API'''
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=texts
    )
    embeddings = [data['embedding'] for data in response['data']]
    return embeddings

def ask_prompt(prompt) -> str:
    logging.info(f'Asking prompt: {prompt[:]}' + '...')
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message['content']

# def add_vectors(vectors, metadata):
    # pass


