import pytest
import asyncio
from app.server.crud.Common import CommonCRUD
from bson import ObjectId

def is_subset_dict(small_dict, large_dict):
    return all(item in large_dict.items() for item in small_dict.items())

@pytest.mark.asyncio()
async def test_round_trip():
    crud = CommonCRUD(collection_name='common')
    doc_to_add = {'name':'name'}
    added_doc = await crud.add(doc_to_add)
    
    assert is_subset_dict(doc_to_add, added_doc)

    added_id = str(added_doc['_id'])
    added_doc = await crud.find_by_id(added_id)

    assert is_subset_dict(doc_to_add, added_doc)

    docs = await crud.find_all()
    assert added_doc in docs

    deleted_count = await crud.delete_by_id(added_id)
    assert deleted_count == 1
    
@pytest.mark.asyncio()
async def test_round_trip_with_ObjectID():
    crud = CommonCRUD(collection_name='common')
    oid_str = '663f0c9a521160f379f3937b'
    doc_to_add = {'test_ids': [ObjectId(oid_str)],
                  'test_id': ObjectId(oid_str)}
    added_doc = await crud.add(doc_to_add)
    
    assert is_subset_dict(doc_to_add, added_doc)

    added_id = str(added_doc['_id'])
    added_doc = await crud.find_by_id(added_id)
    assert added_doc['test_id'] == oid_str
    assert added_doc['test_ids'][0] == oid_str
    assert is_subset_dict(doc_to_add, added_doc)

    docs = await crud.find_all()
    assert added_doc in docs

    deleted_count = await crud.delete_by_id(added_id)
    assert deleted_count == 1
    