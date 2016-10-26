# simple_phonebook
Simple Phonebook

memcached/redis in front

api with commands -> processor

store/lookup function decouple db operations


catalog sqlite

design-only: simple answer: full text search, interesting answer: build a tree index indicating users





Current approach is designed with an SQL database in mind. Particularly sqlite will be used for data storage purposes. Sqlite is easy to use and easy to perform demonstrations with. A production system would require a more sclable database management system such as PostgreSQL. We could even need non-sql databases such as Redis or OpenTSDB depending on particular application and use case.

Following sections will describe the object oriented design of the data model employed for this project.








----

Started out with a classical relation database design, got bored right after generating the object documentation even before writing the table sql schemas. Then I thought of the migrations, which will be necessary for futher improvements (out of the scope of the project) and I stopped with working with the relation database design and switched to a NoSQL design with Redis. So to run the project you will need a redis server running on your local host for testing. I have been dealing with extra load of SQL maintanence for a very long time and NoSQL database systems provide a great alternative storage paradigm.


## Data Model

### Objects

Following sections will describe the main objects designed to store data about the necessary objects and corresponding Redis namespaces.

#### Address Book

Stores all data system keeps about an address book. Key namespace:

addressbook_id_counter, data type: string

addressbook:<address_book_id>:name, data type: string

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

group:<id>:name, data type: string



### Relations

Following sections will describe the namespaces, which will be used to store the relations between the objects described above.

#### Address Book's Persons

Stores relations between person objects and address book objects. Key namespace:

* address_book:<address_book_id>:person:<person_id>, data type string, stores date (GMT Unix timestamp in seconds) user is added to the address book

#### Address Book's Groups

Stores relations between group objects and address book objects. Key namespace:

* address_book:<address_book_id>:group:<group_id>, data type string, stores date (GMT Unix timestamp in seconds) user is added to the address book

#### Person's Street Addresses

Stores relations between person objects and street address objects. Key namespace:

* person:<person_id>:all_street_address_ids, data type: list

#### Person's Email Addresses

Stores relations between person objects and email address objects. Key namespace:

* person:<person_id>:all_email_address_ids, data type: list

#### Person's Phone Numbers

Stores relations between  person objects and phone number objects. Key namespace:

* person:<person_id>:all_phone_number_ids, data type: list

#### Person's Groups

Stores relations between person objects and group objects. Key namespace:

* person:<person_id>:all_group_ids, data type: list

#### Group's Persons

Stores relations between person objects and group objects. Key namespace:

* group:<group_id>:all_persons, data type: hash
