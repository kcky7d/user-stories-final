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
    ("analyst",),
    ("executive assistant",),
    ("data scientist",),
    ("program manager",)
]
c.executemany("INSERT INTO work_roles (name) VALUES (?)", work_roles)

user_stories = [
    ("Awesome Tool", "data scientist", "As a data scientist, I need to be able sum inputs automatically, so I can increase efficiency."),
    ("Horrible Tool", "analyst", "As an analyst, I need to be able to search text in images, so I can search through large documents quickly."),
    ("Great Tool", "executive assistant", "As a executive, I need the ability to send push notifications to my phone, so I can easily keep track fo the backlog."),
    ("Great Tool", "program manager", 	"As a program manager, I need to be able to add my employees to a group, so I can send them mass notifications."),
    ("Great Tool", "data scientist", 	"As a data scientist, I need to perform large calculations on big data sets, so that to perform large calculations on big data sets."),
    ("Great Tool", "data scientist", 	"As a data scientist, I need a tool to quickly calculate standard deviation on data, so that i can focus efforts on other tasks."),
    ("Awesome Tool", "executive assistant", 	"As a executive assistant, I need to be able to write emails with voice , so that i do not have to type as much."),
    ("Horrible Tool", "program manager", 	"As a program manager, I need a tool to group project participants into mail groups, so that i can send one email that reaches all of the required people."),
    ("Horrible Tool", "executive assistant", 	"As a executive assistant, I need to be able to quickly book travel plans with company funds, so that i can make travel plans for important people."),
    ("Horrible Tool", "program manager", 	"As a program manager,  need my daily calendar to show me how far i am from deadlines, so that i can make sure to keep projects on schedule")
]    

c.executemany("INSERT INTO user_stories (tool, work_role, user_story) VALUES (?,?,?)", user_stories)


conn.commit()
conn.close()

print("Database is created and initialized.")
print("You can see the tables with the show_tables.py script.")
