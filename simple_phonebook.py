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
        if con.get('group:'+str(data_value)) is None:
            raise Exception(str('Group ' + str(data_value) + ' not found'))

    else:
        raise Exception(str('Unknown data_field: ' + str(data_field)))

def get_person_str_from_id(person_id):
    sanity_check('person_id', person_id)
    return con.get('person:'+str(person_id)+':first_name') + ' ' + con.get('person:'+str(person_id)+':last_name')

####################################################################################

def create_address_book(address_book_name):
    address_book_id = con.incr('address_book_id_counter')
    con.set('address_book:'+str(address_book_id), address_book_name)
    return address_book_id

def create_person(address_book_id, first_name, last_name, email_address, street_address, phone_number):
    person_id = con.incr('person_id_counter')
    con.set('person:'+str(person_id)+':first_name', first_name)
    con.set('person:'+str(person_id)+':last_name', last_name)
    con.sadd('first_name:'+str(first_name)+':person_ids', person_id)
    con.sadd('last_name:'+str(last_name)+':person_ids', person_id)

    email_address_id = con.incr('email_address_id_counter')
    con.set('email_address:' + str(email_address_id), email_address)
    # TODO: add email address uniqueness validation

    street_address_id = con.incr('street_address_id')
    con.set('street_address:' + str(street_address_id), street_address)

    phone_number_id = con.incr('phone_number_id')
    con.set('phone_number:' + str(phone_number_id), phone_number)

    con.sadd('person:'+str(person_id)+':all_street_address_ids', street_address_id)
    con.sadd('person:'+str(person_id)+':all_email_address_ids', email_address_id)
    con.sadd('person:'+str(person_id)+':all_phone_number_ids', phone_number_id)
    con.sadd('all_email_addresses', str(email_address) + ',' + str(person_id))
    con.sadd('address_book:' + str(address_book_id) + ':person_ids', person_id)

    return [person_id, email_address_id, street_address_id, phone_number_id]

def create_group(address_book_id, group_name):
    group_id = con.incr('group_id_counter')
    con.set('group:'+str(group_id), group_name)
    con.sadd('address_book:' + str(address_book_id) + ':group_ids', group_id)
    return group_id

def add_person_to_group(person_id, group_id):
    sanity_check('person_id', person_id)
    sanity_check('group_id', group_id)
    con.sadd('person:'+str(person_id)+':all_group_ids', group_id)
    con.sadd('group:'+str(group_id)+':all_person_ids', person_id)

def add_person_to_address_book(person_id, address_book_id):
    sanity_check('person_id', person_id)
    sanity_check('address_book_id', address_book_id)
    con.set('address_book:'+str(address_book_id)+':person:'+str(person_id), utc_now_timestamp_sec())

def add_group_to_address_group(group_id, address_book_id):
    sanity_check('group_id', group_id)
    sanity_check('address_book_id', address_book_id)
    con.set('address_book:'+str(address_book_id)+':group:'+str(group_id), utc_now_timestamp_sec())

def get_group_members(group_id):
    sanity_check('group_id', group_id)
    return con.smembers('group:' + str(group_id) + ':all_person_ids')

def get_persons_groups(person_id):
    sanity_check('person_id', person_id)
    return con.smembers('person:'+str(person_id)+':all_group_ids')

def find_person_by_name(*args, **kwargs):
    if 'first_name' in kwargs and 'last_name' not in kwargs:
        return con.smembers('first_name:'+str(kwargs['first_name'])+':person_ids')
    elif 'last_name' in kwargs and 'first_name' not in kwargs:
        return con.smembers('last_name:'+str(kwargs['last_name'])+':person_ids')
    elif 'last_name' in kwargs and 'first_name' in kwargs:
        first_names = con.smembers('first_name:'+str(kwargs['first_name'])+':person_ids')
        last_names = con.smembers('last_name:'+str(kwargs['last_name'])+':person_ids')
        return first_names.intersection(last_names)
    else:
        raise Exception('Can not find last_name or first_name in kwargs')

def find_person_by_email_address(email_address):
    for email_address_person_id in con.smembers('all_email_addresses'):
        if email_address_person_id.startswith(email_address):
            return email_address_person_id.split(',')[1]

    return None

# TODO: removal functions
