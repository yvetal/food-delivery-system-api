from ..database import database
from bson import ObjectId

class CommonCRUD:
    def __init__(self, collection_name):
        self._collection = database.get_collection(collection_name)

    async def add(self, doc: dict):
        await self._collection.insert_one(doc)
        doc['_id'] = str(doc['_id'])

        return doc 

    async def find_by_id(self, id):
        item = await self._collection.find_one({'_id': ObjectId(id)})
        item['_id'] = str(item['_id'])
        return item
    
    async def find_all(self):
        documents = []
        async for document in self._collection.find({}):
            document['_id'] = str(document['_id'])
            documents.append(document)
        return documents

    async def delete_by_id(self, id):
        try:
            deleted = await self._collection.delete_one({'_id': ObjectId(id)})
            return deleted.deleted_count
        except Exception as e:
            return 0