import sqlite3
from sqlite3 import Error
import os



CREATE_TABLE = False
DB_NAME = "pythonsqlite.db"
EMAIL_TABLE_NAME = "email_contact_table"


def create_connection(db_file):
    """Create a database connection to a SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)
    return None


def create_table(conn, table_name, params):
    """Create a table in the SQLite database."""
    try:
        cursor = conn.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                {params}
            )
        """)
        conn.commit()
    except Error as e:
        print(e)


def retrieve_table_schema(conn, table_name, beautify=True):
    """Get the schema of a table in the SQLite database as a string."""
    schema_string = ""
    
    try:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")

        columns = cursor.fetchall()

        if not beautify:
            return columns

        schema_string += f"\nTable Schema for {table_name}:\n\n"
        schema_string += "Column Name   |   Type   |   Not Null\n"
        schema_string += "-" * 40 + "\n"

        for column in columns:
            schema_string += f"{column[1]}   |   {column[2]}   |   {bool(column[3])}\n"

    except Error as e:
        schema_string += str(e)

    return schema_string


def get_database_path():
    current_script_path = os.path.realpath(__file__)
    current_directory = os.path.dirname(current_script_path)
    db_file_path = os.path.join(current_directory, DB_NAME)
    return db_file_path


def add_column(conn, column_name, column_type, table_name):
    try:
        cur = conn.cursor()
        add_column = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"
        cur.execute(add_column)
        return True
    except Error as e:
        print(e)
        return False

def select_data(): 
    conn = create_connection(get_database_path())
    cur = conn.cursor()
    select_entry = f"SELECT * FROM {EMAIL_TABLE_NAME}"
    cur.execute(select_entry)
    cur.fetchall()

rows = select_data()

for row in rows:
     print(dict(row))

'''
def format_query_from_entry_dict(entry_dict):



def add_entry_to_email_table(entry_dict):
    """Add Entry to email_contact_table

    Args:
        entry_dict (_type_): entry dict. The dict key represent the column name and value the data to insert. 
                             if multiple entry need to be inserted, pass a list of value for each keys. 
                             If no value is provided for a key, a NULL value will be inserted in the column.
                             Example : {"name": ["Ewen", "Tom"], "last_name": ["BERNARD", "Jerry"]}
    """
    try:
        conn = create_connection(get_database_path())
        cur = conn.cursor()
        add_entry = f"INSERT INTO {EMAIL_TABLE_NAME} {columns} VALUES {values}"
    except Error as e: 
        print(e)


if __name__ == '__main__':

    connection = create_connection(get_database_path())

    if connection:
        if CREATE_TABLE:
            create_table(connection, 
                         EMAIL_TABLE_NAME, 
                         """id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            last_name TEXT NOT NULL, 
                            reconstructed_email TEXT""")
            add_column(connection, "company_name", "TEXT", EMAIL_TABLE_NAME)
            add_column(connection, "company_domain", "TEXT", EMAIL_TABLE_NAME)
        print(retrieve_table_schema(connection, EMAIL_TABLE_NAME))
        connection.close()
'''