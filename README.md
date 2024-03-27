# Student-Profile-System
This Python-based system manages student profiles, including user registration (admin/student), grades, and extracurricular activities (ECA). It uses text files for storage and provides console-based menus for interaction.  The system offers basic reporting features, with potential for enhancements in security and data handling

# Core Functionalities

## User Management

The system supports two primary user roles:

- **Admin**: Has broad access to manage student data.
- **Student**: Has limited access, primarily to view their own information.

The system stores basic user information:

- ID (unique identifier)
- Username
- Password (stored with basic security, ideally hashed)
- Role

## Student Grades

Grades are stored in a text file (`grades.txt`), with each student's grades on a separate line. Tabular grade reports include:

- Subject
- Grade
- Full Marks (100)
- Subject-wise GPA (on a 4.0 scale)

## Extracurricular Activities (ECA)

ECA activities are stored in a text file (`eca.txt`) with student IDs and a list of their activities. The display is a simple, numbered list of activities for a student.
# Data Structures

- **Users**: Likely stored in a dictionary where keys are student IDs, and values are User objects. Could alternatively be a list of User objects.
- **Grades**: A dictionary where keys are student IDs, and values are dictionaries representing subjects and corresponding grades.
- **ECA**: A dictionary where keys are student IDs and values are lists of ECA activities.

# Interface

- **Console-Based**: The system utilizes a text-based menu for user interaction.
- **Data Display**: The tabulate library is used to provide visually organized tabular output for grades and ECA activities.

# Features

## Admin Dashboard

- Register new users
- Modify student records (update username, password, etc.)
- Delete student records
- Add and modify student grades
- View ECA records for students
- Generate student reports (grades, ECA)

## Student Dashboard

- Update profile (username, password)
- View own grades
- View own ECA Activities
- (Potentially) Add new ECA activities

# Technologies Used

- **Python**: The core programming language.
- **Text Files**: Used for basic data storage.
- **tabulate Library**: For enhancing tabular output.

# Areas for Enhancement

- **Security**: Implement password hashing (e.g., using the bcrypt library) for improved security.
- **Data Persistence**: Consider using a database (like SQLite) for more robust data storage and management.
- **Error Handling**: Add more comprehensive error handling (try-except blocks) to gracefully handle issues like missing files or invalid inputs.
- **Advanced Insights**: Incorporate calculations within the admin dashboard to provide insights on class performance, ECA trends, etc.
- **GUI**: Build a graphical user interface using libraries like Tkinter, PyQt, or web technologies for a more user-friendly experience.
# How to Use Guide

## Run the Application:

1. Make sure you have Python installed.
2. From your terminal (or command prompt), navigate to your project directory.
3. Execute the command: `python main.py`

## Login:

- The system will prompt you for a username and password.
- Use existing admin credentials or register a new admin user.

## Admin Tasks:

Select options from the admin dashboard to:

- Register new students.
- Modify student information.
- Add or edit grades.
- View ECA activities.
- Generate student reports.

## Student Tasks:

Login with student credentials. Use the student dashboard to:

- Update your profile.
- View your grades.
- View and potentially add ECA activities.
