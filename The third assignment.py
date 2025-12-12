from datetime import datetime
import csv
import os

#------------------ Employee Class ------------------

class Employee:
    __employees = []
    __auto_id = 1
    __file_path = "employees.csv"

    def __init__(self, data):
        self.id = Employee.__auto_id
        Employee.__auto_id += 1

        self.emp_id = f"E{self.id:03d}"
        self.name = data.get("name")
        self.joining_date = datetime.strptime(data.get("joining_date"), "%d/%m/%Y").date()
        self.salary = float(data.get("salary"))

    # ------------------ CSV SAVE & LOAD FUNCTIONS ------------------

    @classmethod
    def load_from_csv(cls):
        """Load employees from CSV file on start"""
        if not os.path.exists(cls.__file_path):
            return

        with open(cls.__file_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) != 4:
                    continue

                emp_id, name, joining_date, salary = row

                # Extract auto_id from E###
                num = int(emp_id[1:])
                if num >= cls.__auto_id:
                    cls.__auto_id = num + 1

                obj = cls({
                    "name": name,
                    "joining_date": joining_date,
                    "salary": salary
                })
                obj.emp_id = emp_id  # Keep original ID
                cls.__employees.append(obj)

    @classmethod
    def save_to_csv(cls):
        """Save all employees to CSV after each operation"""
        with open(cls.__file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for emp in cls.__employees:
                writer.writerow([
                    emp.emp_id,
                    emp.name,
                    emp.joining_date.strftime("%d/%m/%Y"),
                    emp.salary
                ])

    #------------------ CRUD OPERATIONS ------------------

    @classmethod
    def create(cls, data):
        obj = cls(data)
        cls.__employees.append(obj)
        cls.save_to_csv()

        print(f"Employee created successfully.")
        print(f"""
            Employee ID number : {obj.emp_id}
            Employee name      : {obj.name}
            Employment History : {obj.joining_date.strftime("%d/%m/%Y")}
            Salary             : {obj.salary}
        """)
        return obj

    @classmethod
    def update(cls, emp_id, data):
        emp = cls.find_by_emp_id(emp_id)
        if not emp:
            print(f"No employee found with emp_id {emp_id}")
            return

        for key, value in data.items():
            if value not in [None, ""]:
                if key == "joining_date":
                    value = datetime.strptime(value, "%d/%m/%Y").date()
                elif key == "salary":
                    value = float(value)
                setattr(emp, key, value)

        cls.save_to_csv()

        print(f"Employee {emp_id} updated successfully.")
        print(f"""
            Employee ID number : {emp.emp_id}
            Employee name      : {emp.name}
            Employment History : {emp.joining_date.strftime("%d/%m/%Y")}
            Salary             : {emp.salary}
        """)

    @classmethod
    def find_by_emp_id(cls, emp_id):
        for emp in cls._Employee__employees:
            if emp.emp_id == emp_id:
                return emp
        return None

    @classmethod
    def delete(cls, emp_id):
        emp = cls.find_by_emp_id(emp_id)
        if emp:
            cls._Employee__employees.remove(emp)
            cls.save_to_csv()
            print(f"Employee {emp_id} deleted successfully.")
        else:
            print(f"No employee found with emp_id {emp_id}")

    @classmethod
    def list(cls, search=None, sort_by=None):
        result = cls._Employee__employees

        if search:
            result = [emp for emp in result if search.lower() in emp.emp_id.lower() or search.lower() in emp.name.lower()]

        if sort_by:
            result.sort(key=lambda e: getattr(e, sort_by))

        print("\n📋 Employee List:")
        print("-" * 60)
        for emp in result:
            print(f"{emp.id:<3} | {emp.emp_id:<6} | {emp.name:<15} | {emp.joining_date} | {emp.salary}")
        print("-" * 60)


#------------------ Validation functions ------------------

def input_name():
    while True:
        name = input("Enter employee name: ").strip()
        if name == "":
            print("Name cannot be empty.")
        else:
            return name

def input_joining_date():
    while True:
        date_str = input("Enter joining date (dd/mm/yyyy): ").strip()
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
            return date_str
        except ValueError:
            print("Invalid date format. Please use dd/mm/yyyy.")

def input_salary():
    while True:
        salary = input("Enter salary: ").strip()
        try:
            val = float(salary)
            if val < 0:
                print("Salary must be positive.")
            else:
                return val
        except ValueError:
            print("Salary must be a number.")

def get_update_data():
    print("Leave field empty to keep current value.")
    data = {}

    name = input("New name: ").strip()
    if name != "":
        data["name"] = name

    joining_date = input("New joining date (dd/mm/yyyy): ").strip()
    if joining_date != "":
        try:
            datetime.strptime(joining_date, "%d/%m/%Y")
            data["joining_date"] = joining_date
        except ValueError:
            print("Invalid date format. Skipping joining date update.")

    salary = input("New salary: ").strip()
    if salary != "":
        try:
            val = float(salary)
            if val < 0:
                print("Salary must be positive. Skipping salary update.")
            else:
                data["salary"] = val
        except ValueError:
            print("Salary must be a number. Skipping salary update.")

    return data


#------------------ Menu --------------------------


def main():
    Employee.load_from_csv()  # <<< LOAD DATA WHEN PROGRAM STARTS

    while True:
        print("""
========= Employee Management =========
1. Create Employee
2. Update Employee
3. Delete Employee
4. List Employees
5. Exit
=======================================
""")
        choice = input("Choose the operation number :").strip()

        if not choice.isdigit():
            print("Please enter a valid number from 0 to 5.")
            continue

        if choice not in [str(i) for i in range(1, 6)]:
            print("Please choose a number from the menu (0 to 11).")
            continue

        if choice == "1":
            emp_data = {
                "name": input_name(),
                "joining_date": input_joining_date(),
                "salary": input_salary()
            }
            Employee.create(emp_data)

        elif choice == "2":
            while True:
                print("\nSearch employee by:")
                print("1. Employee ID")
                print("2. Employee Name")
                print("0. Cancel and return to menu")
                search_choice = input("Enter 1, 2, or 0: ").strip()

                if search_choice == "0":
                    print("Returning to main menu...")
                    break

                if search_choice not in ["1", "2"]:
                    print("Invalid choice. Please enter 1, 2, or 0.")
                    continue

                if search_choice == "1":
                    emp_id = input("Enter employee ID (e.g., E001) or 0 to cancel: ").strip()
                    if emp_id == "0":
                        print("Returning to main menu...")
                        break
                    if len(emp_id) != 4 or not emp_id[1:].isdigit() or emp_id[0].upper() != "E":
                        print("Invalid Employee ID format. Use 'E' followed by 3 digits, e.g., E001.")
                        continue
                    emp = Employee.find_by_emp_id(emp_id.upper())
                    if not emp:
                        print(f"No employee found with emp_id {emp_id}")
                        continue
                    break

                elif search_choice == "2":
                    name = input("Enter employee name or 0 to cancel: ").strip()
                    if name == "0":
                        print("Returning to main menu...")
                        break
                    if not name:
                        print("Employee name cannot be empty.")
                        continue
                    emp = None
                    for e in Employee._Employee__employees:
                        if e.name.lower() == name.lower():
                            emp = e
                            break
                    if not emp:
                        print(f"No employee found with name '{name}'")
                        continue
                    break

            if search_choice == "0" or (locals().get("emp") is None):
                continue

            data = get_update_data()
            Employee.update(emp.emp_id, data)

        elif choice == "3":
            while True:
                emp_id = input("Enter employee ID to delete (e.g., E001) or 0 to cancel: ").strip()

                if emp_id == "0":
                    print("Returning to main menu...")
                    break

                if len(emp_id) != 4 or not emp_id[1:].isdigit() or emp_id[0].upper() != "E":
                    print("Invalid Employee ID format. Use 'E' followed by 3 digits, e.g., E001.")
                    continue

                emp = Employee.find_by_emp_id(emp_id.upper())
                if not emp:
                    print(f"No employee found with emp_id {emp_id}")
                    continue

                confirm = input(f"Are you sure you want to delete employee {emp_id}? (y/n): ").strip().lower()
                if confirm == "y":
                    Employee.delete(emp_id.upper())
                else:
                    print("Delete cancelled.")
                break

        elif choice == "4":
            while True:
                search_option = input("Do you want to search? (y/n): ").strip().lower()
                if search_option in ("y", "n"):
                    break
                print("Invalid input. Please enter 'y' or 'n'.")

            search_term = None
            if search_option == "y":
                search_term = input("Enter search term (emp_id or name): ").strip()
                if not search_term:
                    print("Empty search term entered. Showing all employees.")
                    search_term = None

            while True:
                sort_option = input("Do you want to sort? (y/n): ").strip().lower()
                if sort_option in ("y", "n"):
                    break
                print("Invalid input. Please enter 'y' or 'n'.")

            sort_by = None
            if sort_option == "y":
                while True:
                    print("\nChoose sorting criteria:")
                    print("1. Employee ID")
                    print("2. Name")
                    print("3. Joining Date")
                    print("4. Salary")

                    choice_sort = input("Enter your choice (1-4): ").strip()

                    if not choice_sort.isdigit():
                        print("Please enter a number between 1 and 4.")
                        continue

                    if choice_sort not in ("1", "2", "3", "4"):
                        print("Invalid choice. Please enter 1, 2, 3, or 4.")
                        continue

                    sort_options = {
                        "1": "emp_id",
                        "2": "name",
                        "3": "joining_date",
                        "4": "salary"
                    }

                    sort_by = sort_options[choice_sort]
                    break

            Employee.list(search=search_term, sort_by=sort_by)

        elif choice == "5":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
