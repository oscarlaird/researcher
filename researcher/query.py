# Embed query
# Fetch nearest vectors
# Feed chunks and metadata as context using the metadata id
import logging
import pinecone

from researcher import vector_db
from researcher import sources

def fetch_contexts(q) -> pinecone.QueryResponse:
    '''Fetch contexts from pinecone related to the query'''
    # fetch the nearest vectors from pinecone
    # embed the query
    logging.info(f'Embedding query: {q}')
    v = vector_db.embed_texts([q])[0]
    logging.info('Fetching nearest vectors')
    contexts = vector_db.index.query(vector=v, top_k=2, include_values=False, include_metadata=True)
    return contexts.to_dict()['matches']

def build_prompt(q, contexts):
    '''Build a prompt from the query and contexts'''
    prompt = 'You are writing a clear and concise answer the following question based on the context provided below. Do not use your own knowledge. Your answer must directly quote from the context and you cannot use outside souces of information. \n\n'
    prompt += f'Question: {q}\n'
    prompt += 'Context:\n'
    logging.info(f'Building prompt with {len(contexts)} contexts')
    for context in contexts:
        prompt += f'{context["metadata"]["content"]}\n'
    prompt += 'Answer:'
    return prompt

def query_pipeline(q):
    contexts = fetch_contexts(q)
    prompt = build_prompt(q, contexts)
    return vector_db.ask_prompt(prompt)

