import psycopg2

def delete_table(cursor):
    cursor.execute("""
        DROP TABLE email;
        DROP TABLE phone;
        DROP TABLE name;
    """)

def create_db(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS name(
        name_id SERIAL PRIMARY KEY,
        first_name VARCHAR(40) NOT NULL,
        last_name VARCHAR(40) NOT NULL
    );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS email(
        id SERIAL PRIMARY KEY,
        address VARCHAR(320) NOT NULL,
        name_id INTEGER NOT NULL REFERENCES name(name_id)
    );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS phone(
        id SERIAL PRIMARY KEY,
        number INTEGER NOT NULL,
        name_id INTEGER NOT NULL REFERENCES name(name_id) 
    );    
    """)

def add_new_client(cursor, f_name, l_name, e_address, ph_number=None):
    cursor.execute("""
        INSERT INTO name(first_name, last_name) VALUES(%s, %s) RETURNING name_id;
    """, (f_name, l_name))
    id_new_client = cur.fetchone()

    cursor.execute("""
        SELECT * FROM name;
    """)
    print(cursor.fetchall())

    cursor.execute("""
        INSERT INTO email(address, name_id) VALUES(%s, %s);
    """, (e_address, id_new_client))

    cursor.execute("""
        SELECT * FROM email;
    """)
    print(cursor.fetchall())

    if ph_number != None:
        cursor.execute("""
            INSERT INTO phone(number, name_id) VALUES(%s, %s);
        """, (ph_number, id_new_client))

    cursor.execute("""
        SELECT * FROM phone;
    """)
    print(cursor.fetchall())

def add_phone(cursor, ph_number, cl_id):
    cursor.execute("""
        INSERT INTO phone(number, name_id) VALUES(%s, %s);
    """, (ph_number, cl_id))

    cursor.execute("""
        SELECT * FROM phone;
    """)
    print(cursor.fetchall())

def change_data(cursor, cl_id, f_name=None, l_name=None, e_address=None, ph_number=None):
    if f_name != None:
        cursor.execute("""
            UPDATE name SET first_name=%s WHERE name_id=%s;
        """, (f_name, cl_id))

    if l_name != None:
        cursor.execute("""
            UPDATE name SET last_name=%s WHERE name_id=%s;
        """, (l_name, cl_id))

    cursor.execute("""
        SELECT * FROM name;
    """)
    print(cursor.fetchall())

    if e_address != None:
        cursor.execute("""
            UPDATE email SET address=%s WHERE name_id=%s;
        """, (e_address, cl_id))

    cursor.execute("""
        SELECT * FROM email;
    """)
    print(cursor.fetchall())

    if ph_number != None:
        cursor.execute("""
            UPDATE phone SET number=%s WHERE name_id=%s;
        """, (ph_number, cl_id))

    cursor.execute("""
        SELECT * FROM phone;
    """)
    print(cursor.fetchall())

def delete_phone(cursor, ph_number, cl_id):
    cursor.execute("""
        DELETE FROM phone WHERE number=%s AND name_id=%s;
    """, (ph_number, cl_id,))

    cursor.execute("""
        SELECT * FROM phone;
    """)
    print(cursor.fetchall())

def delete_client(cursor, cl_id):
    cursor.execute("""
        DELETE FROM email WHERE name_id=%s;
    """, (cl_id,))

    cursor.execute("""
        SELECT * FROM email;
    """)
    print(cursor.fetchall())

    cursor.execute("""
        DELETE FROM phone WHERE name_id=%s;
    """, (cl_id,))

    cursor.execute("""
        SELECT * FROM phone;
    """)
    print(cursor.fetchall())

    cursor.execute("""
        DELETE FROM name WHERE name_id=%s;
    """, (cl_id,))

    cursor.execute("""
        SELECT * FROM name;
    """)
    print(cursor.fetchall())

def find_client(cursor, f_name=None, l_name=None, e_address=None, ph_number=None):
    cursor.execute("""
        SELECT n.name_id, n.first_name, n.last_name, e.address, p.number FROM email e
        join name n ON e.name_id=n.name_id
        join phone p ON n.name_id=p.name_id
        WHERE first_name=%s OR last_name=%s OR address=%s OR number=%s;
    """, (f_name, l_name, e_address, ph_number))
    print(cur.fetchall())

with psycopg2.connect(database="client", user="postgres", password="atlant22") as conn:
    with conn.cursor() as cur:
        delete_table(cur)
 
        create_db(cur)

        add_new_client(cur, 'Иван', 'Иванов', 'ivanov@mail.ru', 11111)

        add_new_client(cur, 'Петр', 'Петров', 'petrov@mail.ru', 22222)

        add_phone(cur, 33333, 2)

        change_data(cur, 2, f_name='Семен', l_name='Семенов')

        delete_phone(cur, 11111, 1)

        delete_client(cur, 1)

        find_client(cur, ph_number=22222)

conn.close()