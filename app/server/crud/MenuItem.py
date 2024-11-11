from ..database import database

collection = database.get_collection('MenuItem')

async def retrieve_all():
    documents = []
    async for document in collection.find({}):
        document['_id'] = str(document['_id'])
        documents.append(document)
    return documents

async def add(data: dict) -> dict:
    item = await collection.insert_one(data)
    new_item = await collection.find_one({"_id": item.inserted_id})    
    new_item['_id'] = str(new_item['_id'])
    return new_item