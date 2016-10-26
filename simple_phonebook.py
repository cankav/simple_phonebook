import redis
from datetime import datetime

con = redis.StrictRedis()

# utils ############################################################################
def utc_now_timestamp_sec():
    return (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()

def sanity_check(data_field, data_value):
    if data_field == 'person_id':
        # check user exists
        if con.get('person:'+str(data_value)+':first_name') is None:
            raise Exception(str('Person ' + str(data_value) + ' not found'))

    elif data_field == 'address_book_id':
        # check address book exists
        if con.get('address_book:'+str(data_value)+':name') is None:
            raise Exception(str('Address book ' + str(data_value) + ' not found'))

    elif data_field == 'group_id':
        # check if group exits
        if con.get('group:'+str(data_value)+':name') is None:
            raise Exception(str('Address book ' + str(data_value) + ' not found'))
        
####################################################################################

def add_person(first_name, last_name):
    person_id = con.incr('person_id_counter')
    con.set('person:'+str(person_id)+':first_name', first_name)
    con.set('person:'+str(person_id)+':last_name', last_name)

def add_group(name):
    group_id = con.incr('group_id_counter')
    con.set('group:'+str(group_id)+':name', name)

def add_person_to_group(person_id, group_id):
    sanity_check('person_id', person_id)
    sanity_check('group_id', group_id)
    # overwrites any previous addition operation
    con.hset('group:'+str(group_id)+':all_group_ids', group_id, utc_now_timestamp_sec()) 
    con.set('group:'+str(group_id)+':all_persons', )


def add_person_to_address_book(person_id, address_book_id):
    sanity_check('person_id', person_id)
    sanity_check('address_book_id', address_book_id)

    # store relation
    con.set('address_book:'+str(address_book_id)+':person:'+str(person_id), utc_now_timestamp_sec())

def add_group_to_address_book(group_id, address_book):
    # check group exists
    if con.get('group:'+str(person_id)+':name') is None:
        raise Exception(str('Group ' + str(group_id) + ' not found'))

    # check address book exists
    if con.get('address_book:'+str(address_book_id)+':name') is None:
        raise Exception(str('Address book ' + str(address_book_id) + ' not found'))
    
    # store the relation
    con.set('address_book:'+str(address_book_id)+':group:'+str(group_id>), utc_now_timestamp_sec())
