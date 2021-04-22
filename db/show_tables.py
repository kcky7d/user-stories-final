import sqlite3
import os

db_abs_path = os.path.dirname(os.path.realpath(__file__)) + '/user_stories.db'

conn = sqlite3.connect(db_abs_path)
c = conn.cursor()

def show_user_stories():
    try:
        user_stories = c.execute("""SELECT id, tool, work_role, user_story FROM user_stories""")

        print("Entries")
        print("#############")
        for row in user_stories:
            print("ID:             ", row[0]),
            print("Tool:          ", row[1]),
            print("Work Role:    ", row[2]),
            print("User Stories:          ", row[3]),
            print("\n")
    except:
        print("Something went wrong, please run db_init.py to initialize the database.")
        conn.close()


show_user_stories()

conn.close()
