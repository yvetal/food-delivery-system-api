from ..database import database
from bson import ObjectId
from enum import Enum

class CommonCRUD:
    def __init__(self, collection_name):
        self._collection = database.get_collection(collection_name)

    def _serialize(self, doc):
        if doc:
            for field in doc:
                if field.endswith('_id'):
                    doc[field] = str(doc[field])
                elif field.endswith('_ids'):
                    doc[field] = [str(id) for id in doc[field]]
                elif isinstance(doc[field], Enum):
                    doc[field] = doc[field].value
        return doc
    
    async def add(self, doc: dict):
        doc = self._serialize(doc)
        result = await self._collection.insert_one(doc)
        
        return str(result.inserted_id) 

    async def find_one(self, query):
        doc = await self._collection.find_one(query)
        doc = self._serialize(doc)
        return doc
    
    async def find_by_id(self, id):
        doc = await self.find_one({'_id': ObjectId(id)})
        doc = self._serialize(doc)
        return doc
    
    async def find(self, query):
        docs = []
        async for doc in self._collection.find(query):
            doc = self._serialize(doc)
            docs.append(doc)
        return docs
    
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
    
    async def update_by_id(self, id, update_query):
        
        update_query = self._serialize(update_query)
        result = await self._collection.update_one({'_id': ObjectId(id)}, {'$set': update_query})
        return result.matched_count