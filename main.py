import psycopg2

def delete_table(cursor):
    cursor.execute("""
        DROP TABLE email;
        DROP TABLE phone;
        DROP TABLE name
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
        INSERT INTO email(address, name_id) VALUES(%s, %s);
    """, (e_address, id_new_client))

    cursor.execute("""
        INSERT INTO phone(number, name_id) VALUES(%s, %s);
    """, (ph_number, id_new_client))

def add_phone(cursor, ph_number, cl_id):
    cursor.execute("""
        INSERT INTO phone(number, name_id) VALUES(%s, %s);
    """, (ph_number, cl_id))

def change_data(cursor, cl_id, f_name=None, l_name=None, e_address=None, ph_number=None):
    cursor.execute("""
        UPDATE name SET first_name=%s, last_name=%s WHERE name_id=%s;
    """, (cl_id, f_name, l_name))

    cursor.execute("""
        UPDATE email SET address=%s WHERE name_id=%s;
    """, (cl_id, e_address))

    cursor.execute("""
        UPDATE phone SET number=%s WHERE name_id=%s;
    """, (cl_id, ph_number))

def delete_phone(cursor, ph_number, cl_id):
    cursor.execute("""
        DELETE FROM phone WHERE number=%s AND name_id=%s;
    """, (ph_number, cl_id,))

def delete_client(cursor, cl_id):
    cursor.execute("""
        DELETE FROM email WHERE name_id=%s;
    """, (cl_id,))

    cursor.execute("""
        DELETE FROM phone WHERE name_id=%s;
    """, (cl_id,))

    cursor.execute("""
        DELETE FROM name WHERE name_id=%s;
    """, (cl_id,))

def find_client(cursor, f_name=None, l_name=None, e_address=None, ph_number=None):
    cursor.execute("""
        SELECT * FROM email
        join name USING (name_id)
        join phone USING (name_id)
        WHERE first_name=%s OR last_name=%s OR address=%s OR number=%s;
    """, (f_name, l_name, e_address, ph_number))

with psycopg2.connect(database="client", user="postgres", password="atlant22") as conn:
    with conn.cursor() as cur:
        delete_table(cur)
        conn.commit()

        create_db(cur)
        conn.commit()

        add_new_client(cur, 'Иван', 'Иванов', 'ivanov@mail.ru', 11111)
        conn.commit()

        add_new_client(cur, 'Петр', 'Петров', 'petrov@mail.ru', 22222)
        conn.commit()

        add_phone(cur, 33333, 1)
        conn.commit()

        change_data(cur, 1, ph_number=44444)
        conn.commit()

        delete_phone(cur, 11111, 1)
        conn.commit()

        delete_client(cur, 2)
        conn.commit()

        find_client(cur, l_name='Петров')
        conn.commit()

conn.close()