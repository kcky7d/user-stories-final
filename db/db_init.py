import sqlite3
import os

db_abs_path = os.path.dirname(os.path.realpath(__file__)) + '/user_stories.db'
conn = sqlite3.connect(db_abs_path)
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS tools")
c.execute("DROP TABLE IF EXISTS work_roles")
c.execute("DROP TABLE IF EXISTS user_stories")
print("Tables Dropped")
c.execute("""CREATE TABLE tools(
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    name            TEXT
)""")
print("Table tools created")
c.execute("""CREATE TABLE work_roles(
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    name            TEXT
)""")
print("Table work_roles created")
c.execute("""CREATE TABLE user_stories(
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    tool            TEXT,
                    work_role       TEXT,
                    user_story      TEXT
)""")
print("Table user_stories created")
tools = [
    ("Awesome Tool",),
    ("Great Tool",),
    ("Horrible Tool",)
]
c.executemany("INSERT INTO tools (name) VALUES (?)", tools)

# [(1, 'analyst'), (2, 'executive assistant'), (3, 'data scientist'), (4, 'program manager')]

work_roles = [
    ("Analyst",),
    ("Executive Assistant",),
    ("Data Scientist",),
    ("Program Manager",)
]
c.executemany("INSERT INTO work_roles (name) VALUES (?)", work_roles)

user_stories = [
    ("Awesome Tool", "Data Scientist", "As a data scientist, I need to be able sum inputs automatically, so I can increase efficiency."),
    ("Horrible Tool", "Analyst", "As an analyst, I need to be able to search text in images, so I can search through large documents quickly."),
    ("Great Tool", "Executive Assistant", "As a executive, I need the ability to send push notifications to my phone, so I can easily keep track fo the backlog."),
    ("Great Tool", "Program Manager", 	"As a program manager, I need to be able to add my employees to a group, so I can send them mass notifications.")
]
c.executemany("INSERT INTO user_stories (tool, work_role, user_story) VALUES (?,?,?)", user_stories)


conn.commit()
conn.close()

print("Database is created and initialized.")
print("You can see the tables with the show_tables.py script.")
