import pymongo

# Create the client
client = pymongo.MongoClient('localhost', 27017)

# Connect to our database
db = client['TestBot']

# Fetch our series collection
users_collection = db['users']

def insert_user(collection, data):
    """ Function to insert a user into a collection and
    return the user's id.
    """
    return collection.insert_one(data).inserted_id

new_user = {
    'guid': '123-456',
    'fio': 'Вдовенко Сергей Алексеевич'
}

def find_user(collection, elements, multiple=False):
    """ Function to retrieve single or multiple user from a provided
    Collection using a dictionary containing a user's elements.
    """
    if multiple:
        results = collection.find(elements)
        return [r for r in results]
    else:
        return collection.find_one(elements)
    
def update_user(collection, query_elements, new_values):
    """ Function to update a single user in a collection.
    """
    collection.update_one(query_elements, {'$set': new_values})

id_ = insert_user(users_collection, new_user)
print(id_)

result = find_user(users_collection, {'fio': 'Вдовенко Сергей Алексеевич'})
print(result)

update_user(users_collection, {'_id': id_}, {'fio': 'Вдовенко Сергей Алексеевич 1'})
result = find_user(users_collection, {'_id': id_})
print(result)