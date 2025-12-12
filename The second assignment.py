from datetime import datetime
from collections import defaultdict

# A list to store employee data, each employee stored as a dictionary
employees = []

# Function to add a new employee
def add_employee(): 

    # Automatically generate emp_id based on the largest number currently existing
    if employees:
        max_id = max(int(emp['emp_id']) for emp in employees)
        emp_id = str(max_id +1 )
    else :
        emp_id = '1'

    print(f"The employee number is : {emp_id}")      

    name = input("Enter the employee's name :")   

    # Verify the join date in the format dd/mm/yyyy
    while True:
        joining_date = input("Enter the joining date (dd/mm/yyyy): ")
        try:
            date_obj = datetime.strptime(joining_date, "%d/%m/%Y")
            break
        except ValueError:
            print("Date format is incorrect. Please enter date as dd/mm/yyyy.")   

    # Enter the salary and verify the number
    while True:
        try:
            salary = float(input("Enter the salary: "))
            break
        except ValueError:
            print("Please enter a valid number for salary.")

    department = input("Enter the department name :").strip()

    # Create an employee dictionary and add it to the list
    employee = {
        "emp_id" : emp_id,
        "name" : name,
        "joining_date" : joining_date,
        "salary" : salary,
        "department" : department
    }
    employees.append(employee)
    print("The employee was added successfully!")
    print(f"{employee['emp_id']}, {employee['name']}, {employee['joining_date']}, {employee['department']}, {employee['salary']}")

# Function to display all employees in the list
def show_employees():
    print("\n--- Employee List ---")
    for emp in employees:
        print(f"{emp['emp_id']}, {emp['name']}, {emp['joining_date']}, {emp['department']}, {emp['salary']}")

# Function to display data of a specific employee based on their ID number (emp_id)
def  show_employee_by_id():
    emp_id = input("Enter the employee ID number")
    for emp in employees:
        if emp['emp_id'] == emp_id :
            print(f"{emp['emp_id']}, {emp['name']}, {emp['joining_date']}, {emp['department']}, {emp['salary']}")
            return
    print("The employee was not found !") 

# Function to modify a specific employee's data based on emp_id
def modify_employee():
    emp_id = input("Enter the employee ID number to modify it:")
    for emp in employees:
        if emp['emp_id'] == emp_id :
            name = input("Enter the new name :")   
            while True:
                joining_date = input("Enter the new joining date (dd/mm/yyyy): ")
                try:
                    date_obj = datetime.strptime(joining_date, "%d/%m/%Y")
                    break
                except ValueError:
                   print("Date format is incorrect. Please enter date as dd/mm/yyyy.")  
     

            while True:
                try:
                  salary = float(input("Enter the new salary: "))
                  break
                except ValueError:
                   print("Please enter a valid number for salary.")

            department = input("Enter the new department name :").strip()

            # Update employee data in the dictionary
            emp['name'] = name
            emp['joining_date'] = joining_date
            emp['salary'] = salary
            emp['department'] = department

            print("Employee updated successfully:")
            print(f"{emp['emp_id']}, {emp['name']}, {emp['joining_date']}, {emp['department']}, {emp['salary']}")
            return
    print("The employee was not found !")

# دالة لحذف موظف معين بناءً على emp_id
def delete_employee():
    emp_id = input("Enter the employee ID number to delete it:")
    for emp in employees:
        if emp['emp_id'] == emp_id :
            employees.remove(emp)
            print("The employee has been deleted successfully.")
            return
    print("The employee was not found !")

# A function to search for an employee based on emp_id or name (case-insensitive)
def search_employee():
    query = input("Enter the employee ID number or name")
    for emp in employees: 
        if emp['emp_id'] == query or emp['name'].lower() == query.lower(): 
            print(f"""
                  Employee ID number : {emp['emp_id']},
                  Employee name : {emp['name']},
                  Employment History : {emp['joining_date']},
                  department : {emp['department']},
                  salary : {emp['salary']},
                  """)
            return
    print("The employee was not found !")

# Employee Report in a Coordinated Format (Table)
def employee_report():
    print("\n" + "="*70)
    print("{:<10} {:<15} {:<15} {:<12} {:>10}".format("Emp ID", "Name", "Joining Date", "Department", "Salary"))
    print("-"*70)
    for emp in employees:
        print("{:<10} {:<15} {:<15} {:<12} {:>10.2f}".format(
            emp['emp_id'],
            emp['name'],
            emp['joining_date'],
            emp['department'],
            emp['salary']
        ))
    print("="*70)

# A function to sort employees according to the user's choice (name, salary, date of joining)
def sort_employees(): 
    while True: 
        
        print("""
        ========== Sorting Menu ==========
        1. Sort by name 
        2. Sort by salary 
        3. Sort by joining date
        0. Exit 
        ==================================
        """)

        choice = input("enter number : ")
        if choice == "0":
            break

        if choice == "1":
            key = "name"
        elif choice == "2":
            key = "salary"
        elif choice == "3":
            key = "joining_date"
        else: 
            print("The input is invalid")
            continue

        reverse = input("Descending? (y/n): ").lower() == 'y'
        try:
            sorted_list = sorted(employees, key=lambda x: x[key], reverse=reverse)
            for emp in sorted_list:
                print(emp) 
        except KeyError: 
            print("Invalid sort key.")

# Function to calculate the total salaries of employees in each department and the number of employees in each department
def total_department_salaries(): 
    dept_salaries = defaultdict(float)
    dept_counts = defaultdict(int)

    for emp in employees:
        dept_salaries[emp['department']] += emp['salary']
        dept_counts[emp['department']] += 1

    print("\n" + "="*55)
    print("{:<15} {:>15} {:>20}".format("Department", "Total Salary", "Employee Count"))
    print("-"*55)

    for dept in dept_salaries:
        total = dept_salaries[dept]
        count = dept_counts[dept]
        print("{:<15} {:>15.2f} {:>20}".format(dept, total, count))
    
    print("="*55)

# Function to find the first and last employee to join based on the date
def first_and_last_joined():
    if not employees:
        print("No employees to evaluate.")
        return
    
    # Sorting employees by date of joining
    sorted_by_date = sorted(employees, key=lambda x: datetime.strptime(x['joining_date'], "%d/%m/%Y"))

    while True:
        choice = input("Enter 1 to view the first joined employee, or 2 to view the last joined employee: ").strip()
        
        if choice == '1':
            first = sorted_by_date[0]
            print("\n--- First Joined Employee ---")
            print(f"ID: {first['emp_id']}, Name: {first['name']}, Date: {first['joining_date']}, department: {first['department']}, Salary: {first['salary']}")
            break
        
        elif choice == '2':
            last = sorted_by_date[-1]
            print("\n--- Last Joined Employee ---")
            print(f"ID: {last['emp_id']}, Name: {last['name']}, Date: {last['joining_date']}, department: {last['department']}, Salary: {last['salary']}")
            break
        
        else:
            print("Invalid choice. Please enter 1 or 2.")

# Function to find the employee with the highest and lowest salary
def lowest_and_highest_salary():
    if not employees:
        print("No employees to evaluate.")
        return

    sorted_by_salary = sorted(employees, key=lambda x: x['salary'])

    while True:
        choice = input("Enter 1 to view the highest salary, or 2 to view the lowest salary: ").strip()
        
        if choice == '1':
            highest = sorted_by_salary[-1]
            print("\n--- Highest Salary ---")
            print(f"ID: {highest['emp_id']}, Name: {highest['name']}, Salary: {highest['salary']}, department: {highest['department']}, Joining Date: {highest['joining_date']}")
            break

        elif choice == '2':
            lowest = sorted_by_salary[0]
            print("\n--- Lowest Salary ---")
            print(f"ID: {lowest['emp_id']}, Name: {lowest['name']}, Salary: {lowest['salary']}, department: {lowest['department']}, Joining Date: {lowest['joining_date']}")
            break

        else:
            print("Invalid input. Please enter 1 or 2.")

# The main function that displays the menu and interacts with the user
def main():
    while True :
        print("""
======  Employee Management System ======
0.  Exit
1.  Add an employee
2.  Show all employees
3.  Show employees by id 
4.  modify employee            
5.  delete employee
6.  search employee
7.  sort employees 
8.  employee report
9.  Total salaries of employees in the department
10. First and last joined employees
11. Lowest and highest salary
""")
        choice = input("Choose the operation number :").strip() # The .strip() function is used to remove spaces

        # Input Validation
        if not choice.isdigit(): # Verify that the input number is correct
            print("Please enter a valid number from 0 to 11.")
            continue

        if choice not in [str(i) for i in range(0, 12)]: # To verify that the entered number is within the specified range
            print("Please choose a number from the menu (0 to 11).")
            continue

        if choice == "1" :
            add_employee()
        elif choice == "2" : 
            show_employees()
        elif choice == "3" : 
            show_employee_by_id()
        elif choice == "4" : 
            modify_employee()
        elif choice == "5" : 
            delete_employee()
        elif choice == "6" : 
            search_employee()
        elif choice == "7" : 
            sort_employees()
        elif choice == "8" : 
            employee_report()
        elif choice == "9" : 
            total_department_salaries()
        elif choice == "10" :
            first_and_last_joined()
        elif choice == "11" :
            lowest_and_highest_salary()
        else:
            break

main()