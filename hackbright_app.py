import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    print """\
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)

def get_project_by_title(title):
    query = """SELECT title, description FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    print """\
Project title: %s
Description: %s"""%(row[0], row[1])

def get_student_grade_by_project(title):

    query = """SELECT first_name, last_name, project_title, grade FROM Grades INNER JOIN Students ON (Students.github = Grades.student_github) WHERE project_title = ?"""
    DB.execute(query, (title,))
    rows = DB.fetchall()
   
    for row in rows:
        print """\
        Name: %s %s
        Project Title: %s
        Grade: %d""" % (row[0], row[1], row[2], row[3])

def get_all_grades_for_student(github):
    query = """SELECT first_name, last_name, project_title, grade FROM Students INNER JOIN Grades ON (Students.github = Grades.student_github) WHERE github = ?"""
    DB.execute(query, (github,)) 
    rows = DB.fetchall()
    for row in rows:
        print """\
        Name: %s %s
        Project: %s
        Grade: %d""" % (row[0], row[1], row[2], row[3])
            

def make_new_project(title, description, max_grade):
    query = """INSERT into Projects VALUES(?, ?, ?)"""
    DB.execute(query, (title.strip(), description.strip(), max_grade))
    CONN.commit()
    print "Successfully added project: %s %s" % (title, description)

def update_grade_by_git_proj(new_grade, git_name, proj_title):
    query = """UPDATE Grades SET grade = ?  WHERE Grades.student_github = ? AND Grades.project_title = ?"""
    DB.execute(query,(new_grade, git_name, proj_title))
    CONN.commit()
    print "%s project score in %s successfully updated to %s" %(git_name, proj_title, new_grade)

def main():
    connect_to_db()
    command = None
    print "Please separate your inputs with commas"
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split(", ")
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            if len(tokens) < 2:
                print "You haven't supplied enough information. Enter the github account of the student whose information you would like."
            
            else:
                get_student_by_github(*args)

        elif command == "new_student":
            make_new_student(*args)

        elif command == "project":
            get_project_by_title(*args)
        
        elif command == "get_grades":
            get_student_grade_by_project(*args)

        elif command == "new_project":
            make_new_project(*args)
        elif command == "update_grade":
            update_grade_by_git_proj(*args)

        elif command == "get_all_grades":
            get_all_grades_for_student(*args)

    CONN.close()

if __name__ == "__main__":
    main()
