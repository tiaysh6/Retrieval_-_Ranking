from sentence_transformers import SentenceTransformer, CrossEncoder, util
import numpy as np 
import chromadb
import string

def getResult(query, collection_name):
    PATH= 'Qna_Document\multi-qa-MiniLM-L6-cos-v1'
    model= SentenceTransformer(PATH)
    cross_encoder= CrossEncoder('Qna_Document\ms-marco-MiniLM-L-6-v2')

    client= chromadb.PersistentClient(path="db/")
    Data_Ingestion= client.get_collection(collection_name)

    input_em= model.encode(query).tolist()
    results= Data_Ingestion.query(
        query_embeddings=[input_em],
        n_results=15
    )

    sementic_res= []
    for x in results['documents']:
        for y in x[0:3]:
            sementic_res.append(y)
    

    cross_res= []
    hits= [int(x) for x in results['ids'][0]]
    cross_inp=[[query,results["documents"][0][hit]] for hit in range(15)]
    cross_scores= cross_encoder.predict(cross_inp)
    dis={}
    for i in range(len(cross_scores)):
        dis[results["documents"][0][i]]= cross_scores[i]
    res= sorted(dis.items(),key=lambda x:x[1], reverse=True)
    for i in res[0:3]:
        cross_res.append(i[0])
    

    responce= {}
    responce["SSR"]= sementic_res
    responce["CER"]= cross_res
    return responce
