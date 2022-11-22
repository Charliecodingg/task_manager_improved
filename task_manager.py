#=====importing libraries===========
from datetime import datetime
#this is imported to allow the program to find the current date.
import os
#this is imported to check if a report file already exists.

#=====Functions Section=======
def reg_user():
    #this loop allows the user to add a different username if it is found to be unique
    #if the user doesnt enter a found username then the loop only runs once
    not_duplicate_user = False
    while not_duplicate_user == False:
        new_username = input("Please enter the username to be registered: ")
        usernames = list()
        #first the new username is checked against the current series of usernames as to avoid duplicates
        usernamefile = open('user.txt', 'r+')
        #the file is then looped through to check if the entered values are correct.
        for line in usernamefile:
            #data from the file is converted into a list to be checked.
            currentline = line
            currentline = currentline.replace("\n","")
            currentline = currentline.split(", ")
            #by adding the names that have been checked to a new list
            #an error message can be displayed at the end of checking rather than on every line
            usernames.append(currentline[0])
        if new_username not in usernames:
            not_duplicate_user = True
        else:
            print(f"{new_username} is already taken. Please enter an alternative username: ")
        #If the username is unique then the function asks for their password
        #then writes the information to the users.txt file
    user_registered = False
    usernamefile.close()
    #this loop repeats the password input procedure until both passwords match
    while user_registered == False:
        new_user_password = input("Please enter the new user's password: ")
        password_confirmation = input("Please confirm entered password: ")
        if new_user_password == password_confirmation:
            user_registered = True
        else:
            print("The entered passwords do not match ")
        #the user file is opened in append mode as we are only adding information at the end        
        usernamefile = open('user.txt', 'a')
        usernamefile.write('\n')
        usernamefile.write(f"{new_username}, {new_user_password}")
        #then the user is returned to the while loop of the main menu
        usernamefile.close()
def add_task():
    currentdate = datetime.now()
    taskfile = open('tasks.txt', 'a')
    #the file is opened in append mode as we are only adding data to the end of the file.
    taskfile.write("\n")
    taskfile.write(input("Please enter the user to whom the task is assigned: ") + (", "))
    taskfile.write(input("Please enter the title of the task:" ) + (", "))
    taskfile.write(input("Please enter the description of the task: ") + (", "))
    #to write the date in the desired format the month will be converted to the shortened str
    month_num = currentdate.month
    #this takes the month number from the current date and %m to return the current month
    month_datetime = datetime.strptime(str(month_num), "%m")
    #%b format returns the short name of the month taken form the current time
    month_name = month_datetime.strftime("%b")
    taskfile.write(f"{currentdate.day} {month_name} {currentdate.year}, ")
    taskfile.write(input("Please enter the due date of this task: ") + (", "))
    taskfile.write("No\n") #marks the task as incomplete by default
    taskfile.close()
def view_all():
    taskfile = open('tasks.txt', 'r')
    print("____________________________\n")
    for line in taskfile:
        #checks if the line is empty
        if line != "\n":
            #prints the data for each task in the desired format
            currentline = line
            currentline = currentline.replace("\n", "")
            currentline = currentline.split(", ")
            print(f"Task: \t\t {currentline[1]} ")
            print(f"Assigned to:     {currentline[0]} ")
            print(f"Date assigned:   {currentline[3]} ")
            print(f"Due Date: \t {currentline[4]} ")
            print(f"Task Complete?   {currentline[5]} ")
            print(f"Task Description: \n {currentline[2]}")
            print("\n ____________________________\n")
            #adds a gap after the tasks have displayed to improve clarity for the user
    taskfile.close()
def view_mine(current_username):
    taskfile = open('tasks.txt', 'r')
    Have_task = False
    #this boolean statement is only set to true if the user has a task in the file
    task_selection_dict = {}
    #using a dictionary to build a list of numbers and link them with the tasks assigned to the user
    #so during selection the number used is still linked to the correct task to change
    tasks_count = 0
    #This helps to build the dictionary and keeps the system flexible
    for line in taskfile:
        #checks if the line is empty
        if line != "\n":
            #prints the data for each task in the desired format
            currentline = line
            currentline = currentline.replace("\n", "")
            currentline = currentline.split(", ")
            if currentline[0] == current_username:
                tasks_count += 1
                task_selection_dict[f'{tasks_count}'] = currentline[1]
                #this can be used to 'select' a task by the user and is assigned based on 
                print("____________________________\n")
                print(f"Selection Number: {tasks_count}")
                print(f"Task: \t\t {currentline[1]} ")
                print(f"Assigned to:     {currentline[0]} ")
                print(f"Date assigned:   {currentline[3]} ")
                print(f"Due Date: \t {currentline[4]} ")
                print(f"Task Complete?   {currentline[5]} ")
                print(f"Task Description: \n {currentline[2]}")
                Have_task = True
    if Have_task == False:
            print("\nYou do not have any tasks assigned to you\n")
    else:
            print("\n ____________________________\n")
    taskfile.close()
        #the process of editing and writing the changes to tasks is moved to a new function
        #to improve redability and reduce the amount of indentations
    if Have_task == True:
        task_edit(task_selection_dict)
def task_edit(task_selection_dict):
    #The while loop keeps the user in the menu to select a task to edit or mark complete
    #until they enter -1
    #The ability to edit tasks is only needed if the user has a task to edit
    task_selection = input("Please select a task to edit by entering its Selection Number, Otherwise enter -1 to exit this menu: ")
    while task_selection != '-1':
        if task_selection in task_selection_dict:
            print("1: Mark task complete")
            print("2: Edit task")
            current_task = task_selection_dict[task_selection]
            user_choice = input("Please select an option or enter -1 to return to the task selection menu: ")
            #===========Marking task as complete========
            if user_choice == '1':
                #first the task is found in the file
                taskfile = open('tasks.txt', 'r')
                #replacement maintains the original data in format for the writing portion
                replacement = ""
                for line in taskfile:
                    #avoiding empty lines
                    if line != '\n':
                        currentline = line
                        currentline = currentline.replace("\n", "")
                        currentline = currentline.split(", ")
                        if current_task == currentline[1] and currentline[5] == 'No':
                            #this is only true if we are on the correct line
                            #and the task is marked incomplete
                            #With the task marked complete the file must be written in format
                            update = line.replace(" No", " Yes")
                            print("The task has been updated")
                            replacement = replacement + update
                        elif current_task == currentline[1] and currentline[5] == 'Yes':
                            #if the task is the one selected to edit and also completed
                            #nothing will change and the replacement will change nothing
                            print("This task is already complete")
                            replacement = replacement + line
                        else:
                            #if it is not the correct line the old line is kept as is.
                            replacement = replacement + line
                taskfile.close()
                #opening in write mode
                #the string replacing the old tasks file is written to tasks.txt
                taskfile = open('tasks.txt','w')
                taskfile.write(replacement)
                taskfile.close()
            #============Editing a task section=========
            elif user_choice == '2':
                #first the task is found in the file
                taskfile = open('tasks.txt', 'r')
                #replacement maintains the original data in format for the writing portion
                replacement = ""
                for line in taskfile:
                    #avoiding empty lines
                    if line != '\n':
                        currentline = line
                        currentline = currentline.replace("\n", "")
                        currentline = currentline.split(", ")
                        if current_task == currentline[1] and currentline[5] == 'No':
                            #this is only true if we are on the correct line
                            #and the task is incomplete
                            print("1: The due date ")
                            print("2: The user the task is assigned to ")
                            edit_choice = input("Please select which aspect of the task you would like to edit: ")
                            if edit_choice == '1':
                                new_deadline = input("Please enter a new due date: ")
                                update = line.replace(f"{currentline[4]}", f"{new_deadline}")
                                replacement = replacement + update
                                print("The task's due date has been updated! ")
                            elif edit_choice == '2':
                                new_user_assigned = input("Please enter the username of the person assigned the task: ")
                                update = line.replace(f"{currentline[0]}", f"{new_user_assigned}")
                                replacement = replacement + update
                                print("The user assigned to the task has been updated! ")
                        elif current_task == currentline[1] and currentline[5] == 'Yes':
                            #if the task is the one selected to edit and also completed
                            #nothing will change and the replacement will change nothing
                            print("This task is complete and cannot be edited")
                            replacement = replacement + line
                        else:
                            #if it is not the correct line the old line is kept as is.
                            replacement = replacement + line
                taskfile.close()
                #opening in write mode
                #the string replacing the old tasks file is written to tasks.txt
                taskfile = open('tasks.txt','w')
                taskfile.write(replacement)
                taskfile.close()
            else:
                print("Please select an option: ")
        else:
            print("Please select a valid task")
        task_selection = input("Please select a task to edit by entering its Selection Number, Otherwise enter -1 to exit this menu: ")
def report_gen():
    #============Reading files for information section============
    number_of_tasks = 0
    number_of_complete = 0
    number_of_incomplete = 0
    number_of_users = 0
    number_of_overdue = 0
    currentdate = datetime.now()
    tasks_per_user = {}
    completed_per_user = {}
    incomplete_per_user = {}
    overdue_per_user = {}
    taskfile = open("tasks.txt","r")
    usernamefile = open("user.txt","r")
    #loops through file, adding one to the task count for each non empty line
    for line in taskfile:
        if line != "\n":
            number_of_tasks += 1
            currentline = line
            currentline = currentline.replace("\n", "")
            currentline = currentline.split(", ")
            #this checks if the user assigned to the current task is already in the dictionary
            #if they are one is added to the value linked to their name
            #otherwise they are added and set to one
            if currentline[0] in tasks_per_user:
                tasks_per_user[currentline[0]] += 1
            else:
                tasks_per_user[currentline[0]] = 1
            #the tasks completion status is also counted
            if currentline[5] == "Yes":
                number_of_complete += 1
                #as before this dictionary tracks how many each user has marked as complete
                #linked to their username
                if currentline[0] in completed_per_user:
                    completed_per_user[currentline[0]] += 1
                else:
                    completed_per_user[currentline[0]] = 1
            else:
                #only tasks that are incomplete are checked for their due date
                number_of_incomplete += 1
                #as before this dictionary stores each users amount of incomplete tasks
                if currentline[0] in incomplete_per_user:
                    incomplete_per_user[currentline[0]] += 1
                else:
                    incomplete_per_user[currentline[0]] = 1
                #the due date is stored in a variable to be checked against the current date
                deadline = currentline[4]
                #it is split into each component of the date
                deadline = deadline.split(" ")
                #as the month is in the short name rather than number it needs to be changed
                monthname = deadline[1]
                #it is then cast to an int version of the list alongside the year and day
                intdeadline = list()
                intdeadline.append(int(deadline[0]))
                intdeadline.append(datetime.strptime(monthname, '%b').month)
                #this changes the short name into the integer form of the month
                intdeadline.append(int(deadline[2]))
                #then it must be changed to the datetime type
                #it is entered 2,1,0 because datetime is in the format yyyy mm dd
                deadline_date = datetime(intdeadline[2],intdeadline[1],intdeadline[0])
                if currentdate.date() > deadline_date.date():
                    number_of_overdue += 1
                    #a task is only outstanding if the current date is "smaller" than the deadline
                    #this is also used to build the dictionary of overdue tasks for each user
                    if currentline[0] in overdue_per_user:
                        overdue_per_user[currentline[0]] += 1
                    else:
                        overdue_per_user[currentline[0]] = 1
    taskfile.close()
    usernames = list()
    #loops through file, adding one to the user count for each non empty line
    for line in usernamefile:
        if line != "\n":
            number_of_users += 1
            currentline = line
            currentline = currentline.replace("\n", "")
            currentline = currentline.split(", ")
            usernames.append(currentline[0])
            if currentline[0] not in tasks_per_user:
                tasks_per_user[currentline[0]] = 0
    usernamefile.close()
    #in the case that a user has no associated tasks, they will still be added to tasks per user
    #with no other information in the other dictionaries they will have zero tasks assigned
    #,complete, incomplete or overdue.
    #calculating the percentages of all tasks
    task_incomplete_percentage = (number_of_incomplete/number_of_tasks)*100
    task_overdue_percentage = (number_of_overdue/number_of_tasks)*100
    #==========Generating report files section======
    task_overview_file = open('task_overview.txt','w')
    #this creates the needed file, if it does not already exist
    #if it does exist then it overwrites the old information
    #the information from the Reading files section is then written in a user friendly manner
    #but also in a manner that allows it to be read later in the display_statistics function
    task_overview_file.write((f"Total Number of Tasks: {number_of_tasks}") + ("\n"))
    task_overview_file.write((f"Total Number of Completed Tasks: {number_of_complete}") + ("\n"))
    task_overview_file.write((f"Total Number of Incomplete Tasks: {number_of_incomplete}") + ("\n"))
    task_overview_file.write((f"Total Number of Overdue Tasks: {number_of_overdue}") + ("\n"))
    task_overview_file.write((f"Current Percentage of Incomplete Tasks: {round(task_incomplete_percentage)}%") + ("\n"))
    task_overview_file.write((f"Current Percentage of Overdue Tasks: {round(task_overdue_percentage)}%") + ("\n"))
    task_overview_file.close()
    #The same is now done for the user_overview file
    #using the dictionary values linked to each username as a shared key
    #then dividing by either the total amount or tasks or total amount for the user
    #the multiplying by 100 and rounding to find a clean readable percentage for each category
    user_overview_file = open('user_overview.txt','w')
    for user in tasks_per_user:
        #calculating the percentages for current user, otherwise returns 0 as the percentage
        if user in tasks_per_user:
            user_assigned_percentage = (tasks_per_user[user]/number_of_tasks)*100
            user_assigned_percentage = round(user_assigned_percentage)
        else:
            user_assigned_percentage = 0
        #checks if the user has any completed tasks, otherwise returns 0 as the percentage
        if user in completed_per_user:
            #calculates the percentage of completed tasks for current user from their assigned tasks
            completed_user_percentage = (completed_per_user[user]/tasks_per_user[user])*100
            completed_user_percentage = round(completed_user_percentage)
        else:
            completed_user_percentage = 0
        #checks if the user has any incomplete tasks, otherwise returns 0 as the percentage
        if user in incomplete_per_user:
            #calculates the percentage of incomplete tasks for current user from their assigned tasks 
            incomplete_user_percentage = (incomplete_per_user[user]/tasks_per_user[user])*100
            incomplete_user_percentage = round(incomplete_user_percentage)
        else:
            incomplete_user_percentage = 0
        #checks if the user has any incomplete tasks, otherwise returns 0 as the percentage
        if user in overdue_per_user:
            #calculates the percentage of overdue tasks for the current user from their assigned tasks
            overdue_user_percentage = (overdue_per_user[user]/tasks_per_user[user])*100
            overdue_user_percentage = round(overdue_user_percentage)
        else:
            overdue_user_percentage = 0
        #this writes the information to the file in a user-friendly way
        #that also allows it to be read in the display statistics function
        user_overview_file.write((f"Username: {user}") + (", "))
        user_overview_file.write((f"Total Tasks: {tasks_per_user[user]}") + (", "))
        user_overview_file.write((f"Assigned: {user_assigned_percentage}%") + (", "))
        user_overview_file.write((f"Complete: {completed_user_percentage}%") + (", "))
        user_overview_file.write((f"Incomplete: {incomplete_user_percentage}%") + (", "))
        user_overview_file.write((f"Overdue: {overdue_user_percentage}%") + ("\n"))
    user_overview_file.close()
def display_statistics():
    #this checks if the report files exist, if they do not they are generated before continuing
    if not os.path.exists('user_overview.txt') and not os.path.exists('task_overview.txt'):
        report_gen()
        print("Files not found, Generating reports.")
    else:
        print("Files found")
    #Now the files are certain to exist, so they will be read
    task_overview_file = open('task_overview.txt','r')
    print("____________________________\n")
    print("Task Overview\n")
    for line in task_overview_file:
        if line != '\n':
            print(line)
    task_overview_file.close()
    #Now the stats for each user are displayed
    user_overview_file = open('user_overview.txt','r')
    print("____________________________\n")
    print("User Overview\n")
    for line in user_overview_file:
        if line != '\n':
            currentline = line
            currentline = currentline.split(", ")
            for x in range(len(currentline)):
                print(currentline[x])
                #this prints all the information for each user in a block
            print("____________________________\n")
    user_overview_file.close()
#====Login Section====
usernames = list()
passwords = list()
#Empty lists are created to be appended to later and login defaults to false so the loop begins
login = False
#the login process repeats until the user logs in correctly
while login == False:
    username_input = input("Please enter your username: ")
    password_input = input("Please enter your password: ")
    usernamefile = open('user.txt', 'r+')
#the file is then looped through to check if the entered values are correct.
    for line in usernamefile:
        #data from the file is converted into a list to be checked.
        currentline = line
        currentline = currentline.replace("\n","")
        currentline = currentline.split(", ")
        #by adding the names that have been checked to a new list
        #an error message can be displayed at the end of checking rather than on every line
        usernames.append(currentline[0])
        passwords.append(currentline[1])
        if currentline[0] == username_input:
            if currentline[1] == password_input:
                print("Login Successful ")
                login = True
                currentuser = username_input
                #this is used to check if the user is an admin      
    if not username_input in usernames:
        print("Username not found, Please enter a valid username ")
    if username_input in usernames and not password_input in passwords:
        print("Password incorrect, Please enter the correct password ")
usernamefile.close()
#the file is then closed as it will be opened in a different way when needed.
while login == True:
    #presenting the menu to the user and 
    # making sure that the user input is coneverted to lower case.
    # different options are visible to admin and normal users
#========Menu section=======
    if currentuser == 'admin':
        menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my task
gr - generate reports
ds - display statistics
e - Exit
''').lower()
    else:
        menu = input('''Select one of the following Options below:
a - Adding a task
va - View all tasks
vm - view my task
e - Exit
''').lower()
    #calls the function that registers a new user and writes the entered data to the user.txt file
    #the register user function is only avaliable to the administrator.
    if menu == 'r' and currentuser == 'admin':
        reg_user() 
    #Calls a function that creates a new task from entered data and writes it to the tasks.txt file
    elif menu == 'a':
        add_task()
    #Calls a function that displays all tasks in the tasks.txt file in a user friendly manner
    elif menu == 'va':
        view_all()
    #Calls a function that shows all tasks for the user, or prints a message if they have none.
    #The function also allows them to select tasks to either mark them complete or edit some of their details
    elif menu == 'vm':
        view_mine(currentuser)
    #Calls a function that generates report files based on the tasks and users status
    elif menu == 'gr' and currentuser == 'admin':
        report_gen()
    #Calls a function that displays statistics for the admin by reading report files
    elif menu == 'ds' and currentuser == 'admin':
        display_statistics()
    #exits the program
    elif menu == 'e':
        print('Goodbye!!!')
        exit()
    else:
        print("You have made a wrong choice, Please Try again")