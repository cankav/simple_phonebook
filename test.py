import unittest
from random import random
import redis

from simple_phonebook import create_person
from simple_phonebook import create_group
from simple_phonebook import create_address_book
from simple_phonebook import get_group_members
from simple_phonebook import get_persons_groups
from simple_phonebook import find_person_by_name
from simple_phonebook import add_person_to_group
from simple_phonebook import find_person_by_email_address

con = redis.StrictRedis()

test_param = {
    'first_name' : str(random()),
    'last_name' : str(random()),
    'address_book_name' : str(random()),
    'email_address' : str(random()),
    'street_address' : str(random()),
    'phone_number' : str(random()),
    'group_name' : str(random())
}

                      
class SimplePhoneBookTests(unittest.TestCase):

    def strkey_test(self, key, value):
        db_value = con.get(key)
        self.assertIsNotNone( db_value, 'Key ' + str(key) + ' not found in database' )
        self.assertEqual( db_value, value, 'Value of key ' + str(key) + ' is not correct in database, expected ' + str(value) + ' found ' + str(db_value) )

    def test01_create_addressbook(self):
        test_param['address_book_id'] = create_address_book(test_param['address_book_name'])
        self.strkey_test( 'address_book:'+str(test_param['address_book_id']), test_param['address_book_name'] )
    
    def test02_create_person(self):
        [test_param['person_id'], test_param['email_address_id'], test_param['street_address_id'], test_param['phone_number_id']] = create_person(test_param['address_book_id'], test_param['first_name'], test_param['last_name'], test_param['email_address'], test_param['street_address'], test_param['phone_number'])
        self.strkey_test( 'person:'+str(test_param['person_id'])+':first_name', test_param['first_name'] )
        self.strkey_test( 'person:'+str(test_param['person_id'])+':last_name', test_param['last_name'] )
        self.strkey_test( 'email_address:' + str(test_param['email_address_id']), test_param['email_address'] )
        self.strkey_test( 'street_address:' + str(test_param['street_address_id']), test_param['street_address'] )
        self.strkey_test( 'phone_number:' + str(test_param['phone_number_id']), test_param['phone_number'] )

    def test03_create_group(self):
        test_param['group_id'] = create_group(test_param['address_book_id'], test_param['group_name'])
        self.strkey_test( 'group:' + str(test_param['group_id']), test_param['group_name'] )
        self.assertEqual( con.sismember('address_book:' + str(test_param['address_book_id']) + ':group_ids', test_param['group_id']), 1 )

    def test04_get_group_members(self):
        add_person_to_group(test_param['person_id'], test_param['group_id'])
        self.assertEqual( con.sismember('person:'+str(test_param['person_id'])+':all_group_ids', test_param['group_id']), 1 )
        self.assertEqual( con.sismember('group:'+str(test_param['group_id'])+':all_person_ids', test_param['person_id']), 1 )
        ggm_result = get_group_members(test_param['group_id'])
        expected = set()
        expected.add(str(test_param['person_id']))
        msg='Wrong result from get_group_members expected ' + str(expected) + ' found ' + str(ggm_result) + ' for key group:' + str(test_param['group_id']) + ' :all_person_ids'
        self.assertEqual( ggm_result, expected, msg )

    def test05_get_persons_groups(self):
        expected = set()
        expected.add(str(test_param['group_id']))
        gpg_result = get_persons_groups(test_param['person_id'])
        msg='Wrong result from get_persons_groups expected ' + str(expected) + ' found ' + str(gpg_result) + ' for key person:'+str(test_param['person_id'])+':all_group_ids'
        self.assertEqual( gpg_result, expected, msg )

    def test06_find_person_by_name(self):
        self.assertEqual( find_person_by_name(first_name='nonexistent'), set(), 'first_name nonexistent user should not exist' )
        self.assertEqual( find_person_by_name(last_name='nonexistent'), set(), 'last_name nonexistent user should not exist' )
        self.assertEqual( find_person_by_name(first_name='nonexistent', last_name='nonexistent'), set(), 'first_name/last_name nonexistent user should not exist' )
        self.assertRaises( Exception, find_person_by_name, unknown_parameter='nonexistent' )

        expected=set()
        expected.add(str(test_param['person_id']))

        found=find_person_by_name(first_name=test_param['first_name'])
        self.assertEqual( found, expected, 'find_person_by_name by first name failed, expected ' + str(expected) + ' found ' + str(found) + ' for key ' + 'first_name:'+str(test_param['first_name'])+':person_ids' )

        found=find_person_by_name(last_name=test_param['last_name'])
        self.assertEqual( found, expected, 'find_person_by_name by last name failed, expected ' + str(expected) + ' found ' + str(found) )

        found=find_person_by_name(first_name=test_param['first_name'], last_name=test_param['last_name'])
        self.assertEqual( found, expected, 'find_person_by_name by first name and last name failed, expected ' + str(expected) + ' found ' + str(found) )


    def test06_find_person_by_email_address(self):
        found = find_person_by_email_address('nonexistentemail')
        self.assertIsNone( found, 'nonexistentemail should not exist in database, but found ' + str(found) )

        expected = str(test_param['person_id'])
        found = find_person_by_email_address(test_param['email_address'])
        self.assertEqual( found, expected, 'find_person_by_email_address failed, expected ' + expected + ' found ' + str(found) )

if __name__ == '__main__':
    answer = raw_input('Tests will read/write to your Redis database configured in test.py (make sure simple_phonebook.py has same database connection parameters), are you sure you want to procede? (y/n) ')
    if answer == 'y':
        unittest.main(failfast=True)
    else:
        print 'aborted test'
