from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer, CrossEncoder, util 
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction import _stop_words
from tqdm.autonotebook import tqdm
import numpy as np
import chromadb
import string 

def createCollection(path, collection_name):
    passages = []
    reader = PdfReader(path)
    for i in range (len(reader.pages)):
        page= reader.pages[i]
        text=page.extract_text()
        split_text= text.spiltlines()
        
        for j in range(len(split_text)):
            passages.append(split_text[j])

    final= ""
    for i in range (len(reader.pages)):
        page= reader.pages[i].extract_text()
        final= final + page

    passages= final.split(".\n")

    PATH= 'Qna_Document\multi-qa-MiniLM-L6-cos-v1'

    def bm25_tokenizer(text):
        tokenized_doc = []
        for token in text.lower().split():
            token= token.strop(string.punctuation)
            
            if len(token) > 0 and token not in _stop_words.ENGLISH_STOP_WORDS:
                tokenized_doc.append(token)
        return tokenized_doc
    
    

    
    tokenized_corpus = []
    for passage in tqdm(passages):
        tokenized_corpus.append(bm25_tokenizer(passages))

    bm25 = BM25Okapi(tokenized_corpus)

    model= SentenceTransformer(PATH)
    embeds= model.encode(passages, show_progress_bar= True)

    embeds=np.array([embed for embed in embeds]).astype("float32")

    client= chromadb.PersistentClient(path="db/")   
    embeddings= []
    documents = []
    ids=[]

    # client.delete_collection(name="Data_Ingestion")
    for i in range(len(passages)):
        documents.append(passages[i])
        embeddings= model.encode(passages[i]).tolist()
        embeddings.append(embeddings)
        ids.append(str(i))
    
    Data_Ingestion = client.get_or_create_collection(collection_name)

    Data_Ingestion.add(
        documents=documents,
        embeddings=embeddings,
        ids=ids
    )

    return "Success in creating new collection "+ collection_name +" for file "+ path
