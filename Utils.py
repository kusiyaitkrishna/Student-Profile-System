# This files contains all the function need throughout the application
import os
from Models import User, Student

#Function for generating unique id for new user
def generate_unique_id():
    # Find the maximum existing ID if files exist, else start from 1
    max_id = 0
    if os.path.exists("users.txt"):
        with open("users.txt", "r") as f:
            for line in f:
                id = int(line.strip().split(",")[0])
                max_id = max(max_id, id)
    return max_id + 1

# For loading users
def load_users():
    users = {}
    if os.path.exists("users.txt"):
        with open("users.txt", "r") as f:
            for line in f:
                id, username, password, role = line.strip().split(",")
                users[id] = User(username, password, role, id)
    return users


# Function used to load grades from grades.txt file
def load_grades():
    grades = {}
    if os.path.exists("grades.txt"):
        with open("grades.txt", "r") as f:
            for line in f:
                id, *subject_grades = line.strip().split(",")
                grades[id] = {subject.split(":")[0]: float(subject.split(":")[1]) for subject in subject_grades
                              }
    return grades

# Function for saving grades into grades.txt file
def save_grades(grades):
    with open("grades.txt", "w") as f:
        for id, subjects in grades.items():
            line = f"{
                id}," + ",".join(f"{subject}:{grade}" for subject, grade in subjects.items()) + "\n"
            f.write(line)

# Function for loading eca records from eca.txt file
def load_eca():
    eca_records = {}
    if os.path.exists("eca.txt"):
        with open("eca.txt", "r") as f:
            for line in f:
                id, *activities = line.strip().split(",")
                eca_records[id] = activities
    return eca_records

# Function for saving eca records into eca.txt file
def save_eca(eca_records):
    with open("eca.txt", "w") as f:
        for id, activities in eca_records.items():
            f.write(f"{id},{','.join(activities)}\n")

# For loading passwords
def load_passwords():
    passwords = {}
    if os.path.exists("passwords.txt"):
        with open("passwords.txt", 'r') as f:
            for line in f:
                id, password = line.strip().split(",")
                passwords[id] = password
    return passwords

# For registering new user
def register_user():
    username = input("Enter new username: ")
    password = input("Enter new password: ")
    role = input("Enter role (admin/student): ")

    new_id = generate_unique_id()
    if role == 'student':
        user = Student(username, password, new_id, role=role)
    else:
        user = User(username, password, role, new_id)
    user.save()
    print("Registration successful!")

# For saving users into files
def save_users(users):
    with open("users.txt", 'w') as f:
        for user in users.values():
            f.write(f"{user.id},{user.username},{user.password},{user.role}\n")

# For login Functionality
def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    passwords = load_passwords()
    users = load_users()
    for id, stored_password in passwords.items():
        if stored_password == password and id in users:
            user = users[id]
            if user.role == "student":
                # Load grades and eca
                grades = load_grades()
                eca = load_eca()
                user.grades = grades.get(id, {})
                user.eca = eca.get(id, [])
            return user

    print("Invalid credentials")
    return None

# Importing external libraries for designing the table
import tabulate
# Function for displaying student list in tabular format
def display_student_list(users, sort_by="username", filter_criteria=None):
    students = [(user.id, user.username, user.role)
                for id, user in users.items() if user.role == "student" or user.role == "admin"]

    if filter_criteria:  
        # Example: filter by username containing a substring
        filter_value = filter_criteria.lower()  # Case-insensitive 
        students = [s for s in students if filter_value in s[1].lower()] 

    if sort_by:
        key_index = {"username": 1, "id": 0, "role": 2}.get(sort_by)  
        students.sort(key=lambda x: x[key_index])  

    headers = ["ID", "Username", "Role"]
    print(tabulate.tabulate(students, headers=headers, tablefmt="fancy_grid",stralign=("left", "right", "center")))

# Here is function for displaying eca activities in tabular format
def display_eca_activities():
    eca = load_eca()
    users = load_users()  # Load user data

    if not eca or not users:  # Check if both records exist
        print("ECA and/or User records not found.")
        return

    headers = ["ID", "Username", "ECA Activities"]
    table_data = []

    for student_id, activities in eca.items():
        username = users.get(student_id, "Unknown").username
        table_data.append([student_id, username, ', '.join(activities)])

    print(tabulate.tabulate(table_data, headers=headers, tablefmt="fancy_grid", stralign=("left")))


# Here is function for displaying grades in tabular format
def display_student_grades():
    grades = load_grades()
    users = load_users()

    if not grades or not users:
        print("Grade and/or User records not found.")
        return

    # Determine all subjects
    all_subjects = set()
    for subjects in grades.values():
        all_subjects.update(subjects.keys()) 

    headers = ["ID", "Username"] + list(all_subjects) + ["Total", "Percentage", "GPA"]  
    table_data = []

    for student_id, subjects in grades.items():
        username = users.get(student_id, "Unknown").username 
        row = [student_id, username]
        total_marks = 0
        for subject in all_subjects:
            grade = subjects.get(subject, 0)  # Treat missing grades as 0
            row.append(grade)
            total_marks += grade

        if total_marks:  
            percentage = (total_marks / (len(all_subjects) * 100)) * 100 
        else:
            percentage = 0

        row.extend([total_marks,  "{:.2f}%".format(percentage)])  
        table_data.append(row)

    print(tabulate.tabulate(table_data, headers=headers, tablefmt="fancy_grid", stralign=("left")))

# Here is function for displaying specific student report in tabular format 
def display_student_report(student_id):
    users = load_users()
    grades = load_grades()

    if not all([users, grades]):
        print("User and/or Grade records not found.")
        return

    student = users.get(student_id)
    if not student:
        print(f"Student with ID '{student_id}' not found.")
        return

    # Header 
    print(f"\n**Grade Report for {student.username} (ID: {student_id})**")

    grade_data = [["Subject","Full Marks","Obtain Mark","GPA"]]
    subjects = grades.get(student_id, {})

    total_marks = sum(subjects.values())
   

    for subject, grade in subjects.items():
        grade_data.append([subject,100,grade,  "{:.2f}".format(grade/25)])

    print(tabulate.tabulate(grade_data, headers="firstrow", tablefmt="fancy_grid", stralign=("left")))

# For displaying ECA report of specific student
def display_student_eca(student_id):
    users = load_users()
    eca = load_eca()

    if not all([users, eca]):
        print("User and/or ECA records not found.")
        return

    student = users.get(student_id)
    if not student:
        print(f"Student with ID '{student_id}' not found.")
        return

    print(f"\n**ECA Report for {student.username} (ID: {student_id})**")

    activities = eca.get(student_id, [])
    if activities:
        print(tabulate.tabulate([["ECA Activities"]], headers="firstrow")) # Table Header
        for i, activity in enumerate(activities):
            print(f"{i+1}. {activity}")
    else:
        print("No ECA activities found.")




def admin_dashboard(admin_user):
    while True:
        users = load_users()
        print("\nAdmin Dashboard")
        print("0. View User List")
        print("1. Register User")
        print("2. Modify Student Record")
        print("3. Delete Student Record")
        print("4. Add Grades")
        print("5. Modify Grades")
        print("6. View Grades")
        print("7. Add ECA Activity")
        print("8. Modify ECA Activities")
        print("9. View ECA Activities")
        print("10. Logout")

        choice = input("Enter your choice: ")
        # Display student list
        if choice == '0':
            sort_by = input("Sort by (username, id, role): ").lower()
            display_student_list(users, sort_by)
        # Register new user
        if choice == '1':
            register_user()

         # Modify Student Record
        elif choice == '2': 
            display_student_list(users)
            student_id = input("Enter the student's ID: ")
            users = load_users()
            if student_id in users:
                user = users[student_id]
                if user.role == "student":  # Ensure it's a Student object
                    # Create Student from User data
                    student = Student(**user.__dict__)
                    new_username = input(
                        "Enter new username (leave blank to keep current): ")
                    new_password = input(
                        "Enter new password (leave blank to keep current): ")
                    updates = {}
                    if new_username:
                        updates['username'] = new_username
                    if new_password:
                        updates['password'] = new_password
                    student.update_profile(**updates)
                    users[student_id] = student
                    save_users(users)
                else:
                    print("User is not a student.")
            else:
                print("Student not found")
        # For deleting user from files
        elif choice == '3':
            student_id = input("Enter the student's ID: ")
            users = load_users()
            if student_id in users:
                del users[student_id]  # Delete from users dictionary
                save_users(users)
                # Add calls to delete from grades.txt, eca.txt (explained below)
                print("Student record deleted.")
            else:
                print("Student not found")

        # Here is logic for adding grades or marks for the student
        elif choice == '4':
           
            # For showing lists of students
            display_student_list(users)
            student_id = input("Enter the student's ID: ")
            grades = load_grades()
            new_grades = {}
            subject = ['Maths', 'Physics', 'English', 'Nepali', 'Computer', 'Science']
            num_subjects = 6
            for i in range(num_subjects):
                grade = float(input(f"Enter mark for {subject[i]}: "))
                new_grades[subject[i]] = grade
            grades[student_id] = new_grades
            save_grades(grades)
            print("Grades added successfully.")
        # Here is logic for modifying grades or marks for the student
        elif choice == '5':
            
            student_id = input("Enter the student's ID: ")
            grades = load_grades()
            if student_id in grades:
                print("Existing grades:", grades[student_id])
                subject_to_modify = input("Enter the subject to modify: ")
                if subject_to_modify in grades[student_id]:
                    new_grade = float(input("Enter the new grade: "))
                    grades[student_id][subject_to_modify] = new_grade
                    save_grades(grades)
                    print("Grade modified successfully.")
                else:
                    print("Subject not found.")
            else:
                print("Student not found.")

        # This is for viewing grades of all students
        elif choice == '6':
            display_student_grades()
        
        # This is for adding ECA activity to specific student
        elif choice == '7':
            display_student_list(users)
            student_id = input("Enter the student's ID: ")
            eca = load_eca()
            new_activity = input("Enter the new ECA activity: ")
            eca.setdefault(student_id, []).append(new_activity)
            save_eca(eca)
            print("ECA activity added successfully.")

        # This is for modifying specific student ECA activity
        elif choice == '8':
            student_id = input("Enter the student's ID: ")
            eca =load_eca()
            if student_id in eca:
                print("Existing ECA Records:", eca[student_id])
                activity_index = int(input("Enter the index of the activity to modify: "))
                try:
                    new_activity = input("Enter the new ECA activity: ")
                    eca[student_id][activity_index] = new_activity
                    save_eca(eca)
                    print("ECA activity modified successfully.")
                except IndexError:
                    print("Invalid activity index.")
            else:
                print("Student not found.")

        elif choice == '9':
            display_eca_activities()
        elif choice == '10':
            break
        else:
            print("Invalid choice")


def student_dashboard(student_user):
    while True:
        print("\nStudent Dashboard")
        print("1. Update Profile")
        print("2. View Grades")
        print("3. View ECA")
        print("4. Add ECA Activity")
        print("5. Logout")

        choice = input("Enter your choice: ")

        if choice == '1':  # Modify Student Record
            student_id = input("Enter the student's ID: ")
            users = load_users()
            if student_id in users:
                user = users[student_id]
                if user.role == "student":  # Ensure it's a Student object
                    # Create Student from User data
                    student = Student(**user.__dict__)
                    new_username = input(
                        "Enter new username (leave blank to keep current): ")
                    new_password = input(
                        "Enter new password (leave blank to keep current): ")
                    updates = {}
                    if new_username:
                        updates['username'] = new_username
                    if new_password:
                        updates['password'] = new_password
                    student.update_profile(**updates)
                    users[student_id] = student
                    save_users(users)
                else:
                    print("User is not a student.")
            else:
                print("Student not found")
        # For Displaying grades of specific student
        elif choice == '2':
            student_id = input("Enter the student's ID: ")
            display_student_report(student_id)
        # For displaying ECA activities of specific student
        elif choice == '3':
            student_id = input("Enter the student's ID: ")
            display_student_eca(student_id)
        # For adding ECA activity to specific student
        elif choice == '4':
            display_student_list(users)
            student_id = input("Enter the student's ID: ")
            eca = load_eca()
            new_activity = input("Enter the new ECA activity: ")
            eca.setdefault(student_id, []).append(new_activity)
            save_eca(eca)
            print("ECA activity added successfully.")
         
        elif choice == '5':
            break
        else:
            print("Invalid choice")
