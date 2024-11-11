from ..database import database
from bson import ObjectId

class CommonCRUD:
    def __init__(self, collection_name):
        self._collection = database.get_collection(collection_name)

    def _serialize(self, doc):
        for field in doc:
            if field.endswith('_id'):
                doc[field] = str(doc[field])
            elif field.endswith('_ids'):
                doc[field] = [str(id) for id in doc[field]]
        return doc
    
    async def add(self, doc: dict):
        await self._collection.insert_one(doc)
        doc = self._serialize(doc)

        return doc 

    async def find_by_id(self, id):
        doc = await self._collection.find_one({'_id': ObjectId(id)})
        doc = self._serialize(doc)
        return doc
    
    async def find_all(self):
        docs = []
        async for doc in self._collection.find({}):
            doc = self._serialize(doc)
            docs.append(doc)
        return docs

    async def delete_by_id(self, id):
        try:
            deleted = await self._collection.delete_one({'_id': ObjectId(id)})
            return deleted.deleted_count
        except Exception as e:
            return 0