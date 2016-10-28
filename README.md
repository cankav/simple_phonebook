# simple_phonebook

Started out with a classical relation database design, got bored right after generating the object documentation even before writing the table sql schemas. Then I thought of the migrations, which will be necessary for futher improvements (out of the scope of the project) and I stopped with working with the relation database design and switched to a NoSQL design with Redis. So to run the project you will need a redis server running on your local host for testing. I have been dealing with extra load of SQL maintanence for a very long time and NoSQL database systems provide a great alternative storage paradigm.


## Data Model

### Objects

Following sections will describe the main objects designed to store data about the necessary objects and corresponding Redis namespaces.

#### Address Book

Stores all data system keeps about an address book. Key namespace:

address_book_id_counter, data type: string

address_book:<address_book_id>, data type: string, stores name of the address book

#### Person

Stores all data system keeps about a person. Key namespace:

person_id_counter, data type: string

person:<person_id>:first_name, data type: string

person:<person_id>:last_name, data type: string

#### Street Address

Stores any data about street addresses. Key namespace:

Bstreet_address_id_counter, data type: string

street_address:<id>, data type: string

#### Email Address

Stores any data about email addresses. Key namespace:

email_address_id_counter, data type: string

email_address:<id>, data type: string

#### Phone Number

Stores any data about phone numbers. Key namespace:

phone_number_id_counter, data type: string

phone_number:<id>, data type: string

#### Group

Stores any data about groups. Key namespace:

group_id_counter, data type: string

group:<id>, data type: string, stores name of the group



### Relations

Following sections will describe the namespaces, which will be used to store the relations between the objects described above.

#### Address Book's Persons

Stores relations between person objects and address book objects. Key namespace:

* address_book:<address_book_id>:person_ids, data type: set, stores person_ids of the people recorded in this address book

#### Address Book's Groups

Stores relations between group objects and address book objects. Key namespace:

* address_book:<address_book_id>:group_ids, data type: set, stores group_ids of the groups recorded in this address book

#### Person's Street Addresses

Stores relations between person objects and street address objects. Key namespace:

* person:<person_id>:all_street_address_ids, data type: set, each element of the list stores a street_address_id

#### Person's Email Addresses

Stores relations between person objects and email address objects. Key namespace:

* person:<person_id>:all_email_address_ids, data type: set, each element of the list stores a email_adddress_id

#### Person's Phone Numbers

Stores relations between  person objects and phone number objects. Key namespace:

* person:<person_id>:all_phone_number_ids, data type: set, each element stores a phone_number_id

#### Person's Groups

Stores relations between person objects and group objects. Key namespace:

* person:<person_id>:all_group_ids, data type: set, each element stores a group_id

#### Group's Persons

Stores relations between person objects and group objects. Key namespace:

* group:<group_id>:all_person_ids, data type: set, each element stores a person_id


### Indices

The following namespaces are used to make fast queries.

#### First Name to Person

* first_name:<name>:person_ids, data type: set

#### Last Name to Person

* last_name:<name>:person_ids, data type: set

#### All Email Addresses

* all_email_addresses, data type: set, each element stores a colon delimited string containing email address in first part and person_id in the second.


## API

To use the API, make sure you have a local redis installation and database number zero is available for the purposes of this test. If you would like to use a remote redis server and/or a different db number, you can add parameters to the con=redis.StrictRedis() command. You also need to install the redis python library. Once you have a working redis connection, just download a copy of the repository, import it in your Python shell or code to use the following functions:

As a general rule functions will return None for single values and empty list for list values if requested query is not found in the database.

## simple_phonebook.create_address_book(address_book_name)

Creates a new address book.

## simple_phonebook.create_address_book(address_book_name)

Creates an address book.

## simple_phonebook.create_person(address_book_id, first_name, last_name, email_address, street_address, phone_number)

Adds a person to the address book.

## simple_phonebook.create_group(address_book_id, group_name)

Adds a group to the address book.

## simple_phonebook.get_group_members(group_id)

Given a group we want to returns its members.

## simple_phonebook.get_persons_groups(person_id)

Given a person we want to return the groups the person belongs to.

## simple_phonebook.find_person_by_name(first_name=Foo, last_name=Bar)

Returns persons by name (can supply either first name, last name, or both).

## simple_phonebook.find_person_by_email_address(email_address)

Find person by email address (can supply either the exact string or a prefix string, ie. both "alexander@company.com" and "alex" should work).


## Design-only question

Q. Find person by email address (can supply any substring, ie. "comp" should work assuming "alexander@company.com" is an email address in the address book) - discuss how you would implement this without coding the solution.

A. Substring search calls a for proper searching infrastructure. We could use a SQL database system with fulltext search support. This way we can query the relevant column for any substring. A more modern approach would be to using a general purpose search engine such as Elasticsearch.


## Tests

Go to the simple_python directory and run the test script (python test.py) to run the unit tests.