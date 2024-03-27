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
