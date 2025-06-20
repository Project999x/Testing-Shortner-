#(©)CodeXBotz




import pymongo, os
from config import DB_URI, DB_NAME


dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]


user_data = database['users']
premium_users = database['pros']
clicks = database['click']



async def present_user(user_id : int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user_data.insert_one({'_id': user_id})
    return

async def full_userbase():
    user_docs = user_data.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])
        
    return user_ids

async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})
    return

async def add_pro(user_id: int):
    try:
        premium_users.insert_one({'_id': user_id})
        return True
    except Exception as e:
        print(f"Failed to add admin: {e}")
        return False

async def remove_pro(user_id: int):
    try:
        premium_users.delete_one({'_id': user_id})
        return True
    except Exception as e:
        print(f"Failed to remove admin: {e}")
        return False

async def is_pro(user_id: int):
    return bool(premium_users.find_one({'_id': user_id}))

async def get_pros_list():
    pro_docs = premium_users.find()
    pro_ids = [doc['_id'] for doc in pro_docs]
    return pro_ids

async def add_click(user_id: int, base64_string: str):
    try:
        clicks.update_one(
            {'_id': user_id},
            {'$addToSet': {'base64_strings': base64_string}},
            upsert=True
        )
        return True
    except Exception as e:
        print(f"Failed to store base64 string: {e}")
        return False

async def total_click(base64_string: str):
    try:
        count = clicks.count_documents({'base64_strings': base64_string})
        return count
    except Exception as e:
        print(f"Failed to get total users for base64 string: {e}")
        return 0

