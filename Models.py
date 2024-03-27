# This files contains all the class that need throughout the application
# This is user class
class User:
    def __init__(self, username, password, role, id=None):
        self.username = username
        self.password = password
        self.role = role
        self.id = id

    def save(self):
        with open("users.txt", "a") as f:
            f.write(f"{self.id},{self.username},{self.password},{self.role}\n")
        with open("passwords.txt", "a") as f:
            f.write(f"{self.id},{self.password}\n")
# This is for the student class
class Student(User):
    def __init__(self, username, password, id=None, grades=None, eca=None, role=None):  
        super().__init__(username, password, role, id)
        self.grades = grades or {}
        self.eca = eca or []
    def update_profile(self, **kwargs):
        for key, value in kwargs.items():
            if key in ['username', 'password']:
                setattr(self, key, value)  

    def add_eca(self, activity):
        self.eca.append(activity)

    def view_grades(self):
        if not self.grades:
            print("No grades found.")
        else:
            for subject, grade in self.grades.items():
                print(f"{subject}: {grade}")

    def view_eca(self):
        if not self.eca:
            print("No ECA activities found.")
        else:
            for i, activity in enumerate(self.eca):
                print(f"{i+1}. {activity}")
