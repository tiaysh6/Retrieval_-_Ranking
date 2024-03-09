import chromadb

def getCollection():
    client = chromadb.PersistentClient(path="db/")
    collections = client.list_collections()
    l1=[x.name for x in collections]
    return (l1)

# print (getCollectionList())

