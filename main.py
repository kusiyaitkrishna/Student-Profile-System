#This is entry point of the application
from Utils import login, register_user, admin_dashboard, student_dashboard
def main():
    while True:
        print("\nStudent Profile System")
        print("1. Login")
        print("2. Register")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            user = login()
            if user:
                if user.role == "admin":
                    admin_dashboard(user)
                else:
                    student_dashboard(user)
            else:
                print("Login failed.") 
        elif choice == '2':
            register_user()
        elif choice == '3':
            break  # Exit the program
        else:
            print("Invalid choice.") 

if __name__ == "__main__":
    main()