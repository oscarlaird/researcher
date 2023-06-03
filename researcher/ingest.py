# INGEST
# Download resource from link
# Transcribe the video / download the article
# Chunk it
# Embed
# Insert into pinecone db

from typing import List
from tqdm import tqdm
import logging
from newspaper import Article

from researcher.sources import Session, Source
from researcher import vector_db


def ingest():
    with Session() as session:
        unprocessed_srcs = session.query(Source).filter_by(processed=False).all()
    if not unprocessed_srcs:
        logging.info('No unprocessed sources found')
        return
    logging.info(f'Found {len(unprocessed_srcs)} unprocessed sources')
    print(f'\nProcessing {len(unprocessed_srcs)} sources...')
    for src in tqdm(unprocessed_srcs):
        ingest_src(src)


def ingest_src(src):
    if not src.type:
        with Session() as session:
            src.type = get_type(src)
            session.merge(src)
    if src.type == 'youtube':
        ingest_youtube_video(src)
    elif src.type == 'article':
        ingest_article(src)
    else:
        raise ValueError('No ingestion method for source type ', src.type)


def get_type(src):
    if 'youtube' in src.url:
        return 'video'
    return 'article'


def ingest_article(src):
    # get the content
    # set the metadata
    # chunk
    # embed
    # send to pinecone

    # use the newspaper library to get the content from the article at src.url
    # use the summarizer library to get a summary of the article
    # use the spacy library to get the entities from the article
    # add the content, summary, and entities to the src
    # add the src to pinecone
    assert src.type == 'article', 'src must be an article'
    logging.info(f'Ingesting article at {src.url}')

    article = Article(src.url)
    article.download()
    article.parse()

    logging.info(f'Fetching content from {src.url}')
    src.title = article.title
    src.date = article.publish_date
    content = article.text
    chunks = chunk(content)

    logging.info(f'\nEmbedding {len(chunks)} chunks')
    vectors = vector_db.embed_texts(chunks)
    metadatas = [{'src_id': src.id, 'content': chunk, 'entities': [], 'loc': -1} for chunk in chunks]
    logging.info(f'Adding {len(vectors)} vectors to pinecone')
    vector_db.upsert_vectors(vectors, metadatas)



    # todo: chunk the content, embed the chunks, and add them to pinecone

    with Session() as session:
        # src.processed = True
        session.merge(src)
        session.commit()


# chunk the content into ~200 word chunks of 100 chars
# try to break on sentences
def chunk(content):
    chunks = []
    while content:
        # find the last period before the 500th character
        last_period = content[:1000].rfind('.')
        # if there is no period, just break at 500
        if last_period == -1:
            last_period = 1000
        new_chunk, content = content[:last_period + 1], content[last_period + 1:]
        chunks.append(new_chunk)
    return chunks


# take a youtube video and return a transcript of it with timestamps
def transcribe(youtube_video) -> List[str]:
    pass
    # dl = youtube-dl
    # src.title, src.date = dl....
    # mp4 = dl....
    # chunks = mp4.split(...
    # texts = transcribe(chunks)


def ingest_youtube_video(src):
    # factorization:
    #   text_chunks + timestamps
    #   entities(texts)
    #   vid-metadata: title, date, description/summary, entities
    #   add_to_pinecone

    # texts, timestamps = chunk_yt_vid()
    # vm = vid_metadata()
    # e_lists = search_entities(texts)
    # summary = vm.description + summarize(chunks[0])
    # src.metadata = vm.title, vm.date, summary, set(e for e_list in e_lists for e in e_list)
    # metadatas = [{src_id: src.id, content, entities, timestamp} for content, e_list, timestamp
    # in zip(texts, e_lists, timestamps)]
    # vectors = embed(texts)
    # add_to_pinecone(vectors, metadatas)
    pass
