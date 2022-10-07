import sqlite3
import tkinter.messagebox
from tkinter.ttk import *
from functools import partial
from datetime import datetime, date
from random import randrange
from tkinter import *


'''If this code is going to be run without any of the database files in the directory, then 
you must uncomment the line which calls for create() in functions Films_Database_Initialiser and
Students_Database_Initialiser only once in order to create the database and add value to it.'''

class Error(Exception):
    """This is a base class for other error exceoptions"""
    pass


class UsernameNotUniqueError(Error):
    """Raised when the username is not unique"""
    pass


class EmptyCellsError(Error):
    """Raised when at least one of the required input fields is empty"""
    pass


class InvalidEmailError(Error):
    """Raised when the email address does not contain an @ symbol or has an empty username or domain name"""
    pass


class PasswordsDoNotMatchError(Error):
    """This will come up when the two password entered for the new account do not match"""
    pass


class MainPage(Frame):
    """This is the Main page which opens when the program is run. Allows the user to select whether they
    if they want to login in as a student or teacher"""

    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        # self.background = Label(self.master, image=back_pic)    # This is the background image of the main page
        # self.background.place(x=0, y=0, relwidth=1, relheight=1)
        self.title_label = Label(self.master, font=("Times New Roman", 40, "bold"), bg= "navy blue", fg = "grey",  # This is the main title of the
                                 text="Welcome to Adnan's Cinema Booking System").pack(pady='5')            # mainpage
        self.subtitle_label = Label(self.master, font=("Times New Roman", 16),fg = "black", bg = "light blue",  
                                 text="Select whether you're a Student or a Teacher").pack(pady='5')    # This is a text which guides the
                                                                                                        # user on what button to select
        self.student_button = Button(self.master, font=("Times New Roman", 16), text="Student", bg="light blue",   
                                  command=self.student_window).pack(pady='5')   # This button calls for the function student_window()
                                                                                # which opens the student login page
        self.teacher_button =  Button(self.master, font=("Times New Roman", 16), text="Teacher", bg="navy blue",fg = "grey",   
                                 command=self.teacher_window).pack(pady='5')    # This button calls for the function teacher_window()
                                                                                # which opens the teacher login page
        self.quit = Button(self.master, font=("Times New Roman", 12), text="Quit", bg="black", fg='white',      
                           command=self.close_window).pack(pady='5')     # This button allows the user to close the program
        self.frame.pack()

    def student_window(self):
        self.newWindow = Toplevel(self.master)  # This function opens the new window, the
        self.newWindow.geometry('1096x720')     # student login page after clicking student
        self.app = Student(self.newWindow)
        self.master.withdraw()

    def teacher_window(self):
        self.newWindow = Toplevel(self.master)  # This function opens the new window, the 
        self.newWindow.geometry('1096x720')     # teacher login page, after clicking teacher
        self.app = Teacher(self.newWindow)
        self.master.withdraw()

    def close_window(self):     # This function is in charge of closing the window
        if_yes = tkinter.messagebox.askyesno("Quit", "Are you sure you want to close the program?") # This asks the user if they really
        if if_yes:  # This will check if they had clicked yes or not                            # want to close the program 
            self.master.destroy()
        

class Student(MainPage):
    """This is the GUI for the student login page which opens when clicking the button student"""

    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)         
        # self.background = Label(self.master, image=back_pic)    
        # self.background.place(x=0, y=0, relwidth=1, relheight=1)
        self.frame.grid(row=0, column=0)
        self.student_title = Label(self.master, font=("Times New Roman", 18, "bold"),text="---LOGIN---", bg = "dark blue", fg= "grey")
        self.student_title.grid(row=0, column= 0)
        self.title = Label(self.master, font=("Times New Roman", 16), text='Please enter your Username and Password', bg = "light blue", fg = "black")
        self.title.grid(row=0, column= 1)   # This guides the user on what to do in this page.
        self.user_text = Label(self.master, text="Username:", bg = "light blue", width=15).grid(row=1, column=0, pady='3')
        self.username = Entry(self.master, width=30)    # This is the key variable which temporarily stores  
        self.username.grid(row=1, column=0, columnspan=2, pady='3')   # the user's username and is passed down later
        self.pass_text = Label(self.master, text="Password:", bg = "light blue", width=15).grid(row=2, column=0, pady='3')
        self.password = Entry(self.master, show="*", width=30)
        self.password.grid(row=2, column=0,columnspan=2, pady='3')
        self.checkbox = Checkbutton(self.master, text="Keep me logged in", bg = "black", fg = "grey")   # This is the keep me login feature which
        self.checkbox.grid(row=3, column=0, columnspan=2, pady='3')                                     # one of my stakeholder had requsted for
        
        self.loginbutton = Button(self.master, text="Login", bg="light blue",             # This button allows the user to login
                                  command=self.login).grid(row=4, column=0,columnspan=2, pady='3')  # to their account using the function called login 
                                                                                                    
                                                                                                                     
        self.back = Button(self.master, text="Back", bg ="black", fg= "white",
                           command=self.back).grid(row=4, column=0, pady='3') # This button lets user return to the homepage
        
        self.createnewaccount = Button(self.master, text="Create A New Student Account", bg="dark blue", fg= "grey",   # This buttons directs the user to the 
                                       command=self.create).grid(row=5, column=0, columnspan=2, pady="3")   # NewAccount page using the create function,    
                                                                                                            # which allows a user to create and account  
                                                                                                                  

    def create(self):
        self.newWindow = Toplevel(self.master)  # This function directs the new user to the 
        self.newWindow.geometry('1096x720')     # page which allows them to create another account
        self.app = NewAccount(self.newWindow)
        self.master.withdraw()

    def login(self):    # This function is in charge of allowing the user to login in to their account
        global username
        global password
        
        username = self.username.get()  # This retrieves the username entered in student login page
        password = self.password.get()  # This retrieves the password entered in student login page
        c.execute('SELECT * FROM students WHERE username = ? AND password = ?', (username, password))
        login1 = c.fetchone()   # This checks whether the account info entered is in the students database
        if login1:  
            self.newWindow = Toplevel(self.master)  # If it is found in the database 
            self.newWindow.geometry('1096x720')     # then it opens the students home page 
            self.app = StudentMain(self.newWindow)
            self.master.withdraw()
            tkinter.messagebox.showinfo("-- COMPLETE --", "You Have Now Logged In.", icon="info")   # If it is it will output this message and direct                                                                                        
        else:                                                                                       # them to the student's homepage. 
            tkinter.messagebox.showinfo("-- ERROR --", "Please enter valid infomation!", icon="warning")    # If it doesn't then it will output an error


    def back(self): # This function lets the user return back to the main page
        self.newWindow = Toplevel(self.master)
        self.newWindow.geometry('1096x720')
        self.app = MainPage(self.newWindow)
        self.master.withdraw()


class StudentMain(Student):
    """Student home page. Allows user to update profile, see booking history, and search for films by date"""

    def __init__(self, master):
        global username
        
        self.master = master
        self.frame = Frame(self.master)
        # self.background = Label(self.master, image=back_pic)
        # self.background.place(x=0, y=0, relwidth=1, relheight=1)
        self.frame.pack()        
        self.main_title = Label(self.master, font=("Times New Roman", 40, "bold"), text=("Welcome", username), bg = "dark blue", fg = "grey")
        self.main_title.pack(pady="6")       # This is main title of the student homepage                                
        self.update = Button(self.master, font=("Times New Roman", 16), text="Update Profile", bg="light blue",
                         command=self.Update_Profile_window).pack(pady='5')     # This button calls the function Update_Profile_window
        self.booking_history = Button(self.master, font=("Times New Roman", 16), text="Booking History", bg="light blue",
                         command=self.Booking_History_window).pack(pady='5')    # This button calls the function Booking_History_window
        self.search = Label(self.master, font=("Times New Roman", 16, "bold"),bg="light blue", text='Search for films by date:').pack()
        self.default_date1 = StringVar(self.master)  #This changes the variable to a string
        self.default_date1.set("Monday 12/08/19")  # This is the default value of the option mention
        self.datelist1 = OptionMenu(master, self.default_date1, "Monday 12/08/19", "Tuesday 13/08/19", "Wednesday 14/08/19",
                                    "Thursday 15/08/19", "Friday 16/08/19", "Saturday 17/08/19", "Sunday 18/08/19") 
        self.datelist1.pack()           # This is the option menu which allows you to select the time
        self.searching = Button(self.master, text="Search",bg= "dark blue", fg="grey", 
                                command=self.search_list).pack(pady="5")
        self.log = Button(self.master, font=("Times New Roman", 12), text="Logout", fg="white", bg='black',
                          command=self.logout).pack(pady='5')   # This buttons calls for funtion logout 
                                                                # which allows the user to sign out
    def search_list(self):                            # This function is responsible for searching 
        search_date = self.default_date1.get()   # the movie through the date the user selected   
        c2.execute("""SELECT * FROM movies WHERE               
                            date = ? ORDER BY time='1pm' DESC,
                                                time='2pm' DESC,
                                                time='3pm' DESC,
                                                time='4pm' DESC,
                                                time='5pm' DESC,
                                                time='6pm' DESC,
                                                time='7pm' DESC,
                                                time='8pm' DESC,
                                                time='9pm' DESC,
                                                time='10pm' DESC """, (search_date,))
        # The sqlite3 code above makes a query searching for movies
        output = c2.fetchall()
        self.newWindow = Toplevel(self.master)  # This code directs the user to the window where they can 
        self.newWindow.geometry('1096x720')     # see a list of movies howing from the day they selected                                         
        self.app = SearchResults(self.newWindow, output, search_date)
        self.master.withdraw()

    def Update_Profile_window(self):
        self.newWindow = Toplevel(self.master)
        self.newWindow.geometry('1096x720')
        self.app = StudentProfile(self.newWindow)
        self.master.withdraw()

    def Booking_History_window(self):
        self.newWindow = Toplevel(self.master)
        self.newWindow.geometry('1096x720')
        self.app = BookingHistory(self.newWindow)
        self.master.withdraw()

    def logout(self):
        msg = tkinter.messagebox.askyesno('Logout', 'Are you sure you want to log out?')
        if msg:
            self.newWindow = Toplevel(self.master)
            self.newWindow.geometry('1096x720')
            self.app = MainPage(self.newWindow)
            self.master.withdraw()


class SearchResults(Student):
    """This class is responsible for displaying the list of movies which shows on
    the day of that which the user had selected in the student home page"""
    
    def __init__(self, master, output, search_date):    # I passed down the variables output and search_date 
        self.search_date = search_date                  # from the StudentMain class
        self.master = master
        self.output = output
        self.frame = Frame(self.master)    
        # self.background = Label(self.master, image=back_pic)
        # self.background.place(x=0, y=0, relwidth=1, relheight=1)
        self.frame.grid(row=0, column=0)
        self.date = Label(self.master, text='Date',  bg="dark blue", fg="grey",font=("Times New Roman", 16, "bold"), width=8)
        self.date.grid(row=0, column=1, pady='1')   # This is the header for which the
                                                    # date of the movie is displayed under
        self.time = Label(self.master, text='Time', bg="dark blue", fg="grey", font=("Times New Roman", 16, "bold"), width=6)
        self.time.grid(row=0, column=2, pady='1')   # This is the header for which the
                                                    # time of the movie is displayed under
        self.title = Label(self.master, text='Title',  bg="dark blue", fg="grey", font=("Times New Roman", 16, "bold"), width=15)
        self.title.grid(row=0, column=3, pady='1')  # This is the header for which the
                                                    # title of the movie is displayed under
        self.description = Label(self.master, text='Description',  bg="dark blue", fg="grey", font=("Times New Roman", 16, "bold"), width=30)
        self.description.grid(row=0, column=4, pady='1')    # This is the header for which the
                                                            # description of the movie is displayed under                                                                                                         
        self.booked = Label(self.master, text='Booked',  bg="dark blue", fg="grey", font=("Times New Roman", 16, "bold"), width=8)
        self.booked.grid(row=0, column=5, pady='1') # This is the header for where you get the        
        self.available = Label(self.master, text='Available', bg="dark blue", fg="grey", font=("Times New Roman", 16, "bold"), width=8)
        self.available.grid(row=0, column=6, pady='1')  # This is the header for where it tells the user
                                                        # how many available seats there are
        self.book = Label(self.master, text='Book ticket',  bg="dark blue", fg="grey", font=("Times New Roman", 16, "bold"), width=12)
        self.book.grid(row=0, column=7, pady='1')   # This is the header for which the
                                                    # user can book ticket for the movie.
        
        
        widths = (15, 6, 35, 60, 8, 8, 12)
        for i in self.output:       # This double for loop is used to to display   
            for j in i:                   # the film details under each of the headers
                infos = Label(self.master, text=j, bg="light blue", font=("Times New Roman", 6), width=widths[i.index(j)])
                infos.grid(row=output.index(i) + 1, column=i.index(j) + 1, pady='1')
            self.taken = i[4]   # This shows the number of people that have booked this movie alreadt
            self.datetime7 = (i[0], i[1])   # This is the array for the date and the time of the movie.
            self.book_now = Button(self.master, bg="light blue", text='Book', command=partial(self.book_movie, self.taken, self.datetime7),
                       font=("Times New Roman", 7))     # Using a partial here allows a function to be claled in a button 
                                                        # with a parameter without the function being called automatically   
            self.book_now.grid(row=output.index(i) + 1, column=7, pady='1')
        self.back = Button(self.master, font=("Times New Roman", 12), text="Back", bg="black", fg="white",
                           command=self.back).grid(row=10, column=1, pady='1')  # This buton calls for the function back() which returns to the student home page.

    def book_movie(self, taken, datetime7):
        book_yes = tkinter.messagebox.askyesno('Book', 'Do you want to confirm this booking?')
        if book_yes:     
            self.taken = taken    
            self.datetime = datetime7            
            c3.execute("""SELECT * FROM bookings WHERE username = ? AND date = ? AND time = ?""",
                       (username, self.datetime[0], self.datetime[1]))  # This select query is made to check  
            already_booked = c3.fetchone()                              # whether the user already booked the movie
            if already_booked:      # An IF statement for if the user had already booked this movie
                tkinter.messagebox.showinfo("---- ERROR ----", "You are already booked into this film", icon="warning")
            elif self.taken == 100:     # An IF statement for if the cinema is fully booked
                tkinter.messagebox.showinfo("---- ERROR ----", "Movie showing full", icon="warning")
            else:
                today_hour = datetime.today().hour - 12     # This code sets todays date and 
                today_day = date.today().day                # time with newer variable names
                today_month = date.today().month
                today_year = date.today().year
                new_time = int(self.datetime[1][:-2])   # This is the time of the movie
                temporary_date = self.datetime[0].split()
                new_date = int(temporary_date[1][:2])    # This is the date of the movie
                
                if today_year > 2019 or \
                        today_year == 2019 and today_month > 8 or \
                        today_year == 2019 and today_month == 8 and today_day > new_date or \
                        today_year == 2019 and today_month == 1 and today_day == new_date and today_hour >= new_time:
                    tkinter.messagebox.showinfo("---- ERROR ----", "Date and time of showing has passed!",
                                                icon="warning")     # This if statements checks whether the current
                else:                                               # time has passed the movie showing time
                    with conn2:     # If the other conditions of the statement isn't met, then the movie database gets updated
                        c2.execute('''UPDATE movies SET booked = ?, available = ? WHERE       
                        date = ? AND time = ?''', (self.taken + 1, 100 - (self.taken + 1), datetime7[0], datetime7[1]))
                    self.newWindow = Toplevel(self.master)
                    self.newWindow.geometry('1096x720')
                    self.app = Booked(self.newWindow, self.datetime)
                    self.master.withdraw()

    def back(self):     # This function returns the user to the student home page
        self.newWindow = Toplevel(self.master)
        self.newWindow.geometry('1096x720')
        self.app = StudentMain(self.newWindow)
        self.master.withdraw()


class StudentProfile(StudentMain):  
    '''This is the page which allows the student to update their profile'''

    def __init__(self, master):     
        self.master = master
        self.frame = Frame(self.master)
        # self.background = Label(self.master, image=back_pic)
        # self.background.place(x=0, y=0, relwidth=1, relheight=1)
        self.frame.grid(row=0, column=0)
        c.execute('SELECT * FROM students WHERE username = ?', (username,)) # Searches for the user's information because this information 
        self.output = c.fetchone()                                          # will be used in this class to display the user's account profile
        self.title = Label(self.master, text="Please update your details below:", bg="dark blue", fg="grey", font=("Times New Roman", 16, "bold"))
        self.title.grid(row=0, column=0, columnspan=2, pady='3')    # Main title of the page guiding the user on what to do in this page
                                                                                                             
        self.first = Label(self.master, text="First Name:",bg="light blue", width='15').grid(row=1, column=0, pady='3')
        self.firstname = Entry(self.master, width='30') # Used the widget entry to alow the user to
        self.firstname.insert(END, self.output[0])      # change the field and inserted the current 
        self.firstname.grid(row=1, column=1, pady='3')  # field in the student's database   

        self.last = Label(self.master, text="Last Name:", bg="light blue", width='15').grid(row=2, column=0, pady='3')
        self.lastname = Entry(self.master, width='30')  
        self.lastname.insert(END, self.output[1])
        self.lastname.grid(row=2, column=1, pady='3')

        self.email = Label(self.master, text="Email Address:", bg="light blue", width='15').grid(row=3, column=0, pady='3')
        self.email_add = Entry(self.master, width='30')
        self.email_add.insert(END, self.output[2])
        self.email_add.grid(row=3, column=1, pady='3')

        self.age_text = Label(self.master, text="Age:", bg="light blue", width='15').grid(row=4, column=0, pady='3')
        self.age = Entry(self.master, width='30')
        self.age.insert(END, self.output[3])
        self.age.grid(row=4, column=1, pady='3')

        self.password_1 = Label(self.master, text="Password:", bg="light blue",width='15').grid(row=5, column=0, pady='3')
        self.firstpassword = Entry(self.master, width='30', show='*')   # I hid the password to allow the account to be secure
        self.firstpassword.insert(END, self.output[5])
        self.firstpassword.grid(row=5, column=1, pady='3')

        self.password_2 = Label(self.master, text="Confirm Password:", bg="light blue", width='15').grid(row=6, column=0, pady='3')
        self.secondpassword = Entry(self.master, width='30', show='*')
        self.secondpassword.insert(END, self.output[5])
        self.secondpassword.grid(row=6, column=1, pady='3')

        self.update = Button(self.master, text="Update Details",font=("Times New Roman", 12, "bold"), bg="dark blue", fg="grey",
                             command=self.change).grid(row=7, columnspan=2, pady='3')   # This button calls for the functio change

        self.back = Button(self.master, font=("Times New Roman", 12), text="Back", fg="white", bg='black',
                           command=self.back).grid(row=8, column=0, pady='3')
        self.log = Button(self.master, font=("Times New Roman", 12), text="Logout", fg="white", bg='black',
                          command=self.logout).grid(row=8, column=1, pady='3')

    def change(self):   # This function is responsible for updating the user's account information
        ask_yes = tkinter.messagebox.askyesno('Update Profile', 'Confirm changes?')
        if ask_yes:
            new_first = self.firstname.get()    # Retrieves the data in the entry fields 
            new_last = self.lastname.get()      # which the user might have changed
            new_email = self.email_add.get()
            new_age = self.age.get()
            new_firstpassword = self.firstpassword.get()
            new_secondpassword = self.secondpassword.get()

            try:    
                if not new_first or not new_last or not new_email or not new_age:
                    raise EmptyCellsError       # This would verify the data being used to update the  
                new_age = int(new_age)          # student's account to confirm whether or not the data is valid
                if new_age < 0:
                    raise ValueError
                if '@' and '.'  in new_email:
                    at = new_email.split('@')
                    full_stop = at[1].split('.')    # This splits the email into 3 parts
                    if not (at[0] and full_stop[0] and full_stop[1]):
                        raise InvalidEmailError
    
                else:
                    raise InvalidEmailError
                if new_firstpassword != new_secondpassword: 
                    raise PasswordsDoNotMatchError

            except EmptyCellsError: 
                tkinter.messagebox.showinfo("---- ERROR ----", "Please fill in all of the cells.", icon="warning")
            except InvalidEmailError:           # These are the pop up messages which will 
                tkinter.messagebox.showinfo("---- ERROR ----", "Invalid email format!", icon="warning")
            except PasswordsDoNotMatchError:    # display depending on which type of error it is
                tkinter.messagebox.showinfo("---- ERROR ----", "Passwords do not match!", icon="warning")
            except ValueError:
                tkinter.messagebox.showinfo("---- ERROR ----", "Invalid age format!", icon="warning")
            else:
                with conn:  # The sqlite code below updates the user's personl details in the student database
                    c.execute("""UPDATE students
                            SET first = ?,
                                last = ?,
                                email = ?,
                                age = ?,
                                password = ?
                            WHERE username = ?""",
                              (new_first, new_last, new_email, new_age, new_firstpassword, username))
                self.newWindow = Toplevel(self.master)
                self.newWindow.geometry('1096x720')
                self.app = StudentProfile(self.newWindow)
                self.master.withdraw()
                tkinter.messagebox.showinfo("---- SUCCESSFUL ----", "Profile successfully updated.",
                                            icon="info")

    def back(self):
        self.newWindow = Toplevel(self.master)
        self.newWindow.geometry('1096x720')
        self.app = StudentMain(self.newWindow)
        self.master.withdraw()


class NewAccount(Student):
    '''This is the class which is responsible for allowing a new user to
    create an account'''
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        # self.background = Label(self.master, image=back_pic)
        # self.background.place(x=0, y=0, relwidth=1, relheight=1)
        self.frame.grid(row=0, column=0)

        self.title = Label(self.master, text="Please enter your details below:", bg="dark blue", fg="grey", font=("Times New Roman", 16, "bold"))
        self.title.grid(row=0, column=0, columnspan=2, pady='3')    # The main title of the page which guides 
                                                                    # the user on what to do in the page                                                                                                                                                                                                                                                                                                                                        
        self.firstname = Label(self.master, text="First Name:", bg="light blue", width='15').grid(row=1, column=0, pady='3')
        self.firstname_entry = Entry(self.master, width='30')     # Entry field for the user to 
        self.firstname_entry.grid(row=1, column=1, pady='3')      # enter in their first name

        self.lastname = Label(self.master, text="Last Name:", bg="light blue", width='15').grid(row=2, column=0, pady='3')
        self.lastname_entry = Entry(self.master, width='30')      # The entry field for the user 
        self.lastname_entry.grid(row=2, column=1, pady='3')       # to enter in their last name

        self.email = Label(self.master, text="Email Address:", bg="light blue", width='15').grid(row=3, column=0, pady='3')
        self.email_entry = Entry(self.master, width='30')       # The entry field for the user
        self.email_entry.grid(row=3, column=1, pady='3')        # to enter in their email

        self.age = Label(self.master, text="Age:", bg="light blue", width='15').grid(row=4, column=0, pady='3')
        self.age_entry = Entry(self.master, width='30')         # The entry field for the user
        self.age_entry.grid(row=4, column=1, pady='3')          # to enter in their age

        self.newusername = Label(self.master, text="Username:", bg="light blue", width='15').grid(row=5, column=0, pady='3')
        self.new_username_entry = Entry(self.master, width='30')    # The entry field for the user
        self.new_username_entry.grid(row=5, column=1, pady='3')     # to enter in their username

        self.new_password1 = Label(self.master, text="Password:", bg="light blue", width='15').grid(row=6, column=0, pady='3')
        self.new_password1_entry = Entry(self.master, width='30', show="*")    # The entry field for the user 
        self.new_password1_entry.grid(row=6, column=1, pady='3')               # to enter in their password

        self.new_password2 = Label(self.master, text="Confirm Password:", bg="light blue", width='15').grid(row=7, column=0, pady='3')
        self.new_password2_entry = Entry(self.master, width='30', show="*")    # The entry field for the user to
        self.new_password2_entry.grid(row=7, column=1, pady='3')               # re-enter in their password

        self.create = Button(self.master, font=("Times New Roman", 10, "bold"),text="Create new account", bg="dark blue", fg="grey", command=self.change)
        self.create.grid(row=8, columnspan=2, pady='3')     # This button calls for the function change

        self.back = Button(self.master, font=("Times New Roman", 9), text="Back", fg="white", bg='black',
                           command=self.back).grid(row=9, column=0, pady='3')   # This button calls for the function back 
                                                                                # which returns the user to the login page
                                                                                
    def change(self):
        # This function is similar to the one that is in the class StudentProfile
        new_first = self.firstname_entry.get()  # These retrieves the information in the entry 
        new_last = self.lastname_entry.get()    # fields and store them under new variable names
        new_email = self.email_entry.get()
        new_age = self.age_entry.get()
        new_username = self.new_username_entry.get()
        new_password1 = self.new_password1_entry.get()
        new_password2 = self.new_password2_entry.get()
        try:
            if not new_first or not new_last or not new_email or not new_age or not new_username or not new_password1 or not new_password2:
                raise EmptyCellsError       # These codes are the same as the 
            new_age = int(new_age)          # one in the StudentProfile class
            if new_age < 0:
                raise ValueError
            if '@' and '.' in new_email:
                s = new_email.split('@')
                t = s[1].split('.')
                if not (s[0] and t[0] and t[1]):
                    raise InvalidEmailError
            else:
                raise InvalidEmailError
            if new_password1 != new_password2:
                raise PasswordsDoNotMatchError
            c.execute('SELECT * FROM students WHERE username = ?', (new_username,))
            # This is a new code and this look for a username in the database
            # student which is the same as the one inputted by the new user
            possibleunique = c.fetchone()  
            if possibleunique:              
                raise UsernameNotUniqueError       

        except EmptyCellsError:
            tkinter.messagebox.showinfo("---- ERROR ----", "Please fill in all of the cells.", icon="warning")
        except InvalidEmailError:       # These are the message box which would display 
            tkinter.messagebox.showinfo("---- ERROR ----", "Invalid email format!", icon="warning")
        except UsernameNotUniqueError:  # if this function detects any of these errors
            tkinter.messagebox.showinfo("---- ERROR ----", "Username already taken!", icon="warning")
        except PasswordsDoNotMatchError:
            tkinter.messagebox.showinfo("---- ERROR ----", "Passwords do not match!", icon="warning")
        except ValueError:
            tkinter.messagebox.showinfo("---- ERROR ----", "Invalid age format!", icon="warning")
        else:   # If there is no errors in the details with the details provided this will happen
            with conn:
                c.execute("""INSERT INTO students VALUES (?, ?, ?, ?, ?, ?)""",
                          (new_first, new_last, new_email, new_age, new_username, new_password1))
                # The code above inserts the user's details into a the student's database under a new field record    
            self.newWindow = Toplevel(self.master)
            self.newWindow.geometry('1096x720')
            self.app = Student(self.newWindow)
            self.master.withdraw()
            tkinter.messagebox.showinfo("---- SUCCESSFUL ----", "Account successfully created.",
                                        icon="info")    # This message box is appeared to let the user know 
                                                        # that they have successfully created a new account                       
    def back(self):
        self.newWindow = Toplevel(self.master)
        self.newWindow.geometry('1096x720')
        self.app = Student(self.newWindow)
        self.master.withdraw()


class Booked(StudentProfile, SearchResults):
    """"This class is responsible for the design of the page where it
    shows the booking details, which includes the seat number for the student, for the movie"""
    def __init__(self, master, datetime1):
        self.datetime1 = datetime1      # This is the date and time of
        self.master = master            # the movie which was booked
        self.frame = Frame(self.master)
        # self.background = Label(self.master, image=back_pic)
        # self.background.place(x=0, y=0, relwidth=1, relheight=1)
        self.frame.grid(row=0, column=0, pady='1')

        c.execute('SELECT * FROM students WHERE username = ?', (username,))
        self.output = c.fetchone()  # This is to retrieve the student's information 
                                    # so I can display their information in the page         
        self.heading = Label(self.master, text='Booking successful! booking details are below:', bg="dark blue", fg="grey", width=45,
                             font=("Times New Roman", 16,"bold")).grid(row=0, columnspan=2, pady='5')
        
        self.first = Label(self.master, text="First Name:", bg="dark blue", fg="grey",  width=15).grid(row=1, column=0, pady='3')
        self.firstname = Label(self.master, text=self.output[0], bg="light blue", width=30)
        self.firstname.grid(row=1, column=1, pady='3')  # This displays the user's first name 
                                                        # by calling the first field in output 
        self.last = Label(self.master, text="Last Name:", bg="dark blue", fg="grey", width=15).grid(row=2, column=0, pady='3')
        self.lastname = Label(self.master, text=self.output[1], bg="light blue", width=30)
        self.lastname.grid(row=2, column=1, pady='3')   # This displays by calling user's last name
                                                        # by calling the second
        self.email = Label(self.master, text="Email Address:", bg="dark blue", fg="grey", width=15).grid(row=3, column=0, pady='3')
        self.emailadd = Label(self.master, text=self.output[2], bg="light blue", width=30)
        self.emailadd.grid(row=3, column=1, pady='3')   # This displays by calling user's email
                                                        # by calling the third field in output
        self.age_title = Label(self.master, text="Age:", bg="dark blue", fg="grey", width=15).grid(row=4, column=0, pady='3')
        self.age = Label(self.master, text=self.output[3], bg="light blue", width=30)
        self.age.grid(row=4, column=1, pady='3')        # This displays by calling user's age
                                                        # by calling the fourth field in output
        self.date_title = Label(self.master, text="Date:", bg="dark blue", fg="grey", width=15).grid(row=5, column=0, pady='3')
        self.date = Label(self.master, text=self.datetime1[0], bg="light blue", width=30)
        self.date.grid(row=5, column=1, pady='3')       # This displays by calling user's 
                                                        # by calling the fifth field in output
        self.time_title = Label(self.master, text="Time:", bg="dark blue", fg="grey", width=15).grid(row=6, column=0, pady='3')
        self.time = Label(self.master, text=self.datetime1[1], bg="light blue", width=30)
        self.time.grid(row=6, column=1, pady='3')

        c2.execute('''SELECT booked FROM movies WHERE
                    date = ? AND time = ?''', (self.datetime1[0], self.datetime1[1]))
        numb = str(c2.fetchone()[0])    # This converts the date of the movie into a string
        if len(numb) == 1:    
            numb = '0' + str(numb)
        numb0 = int(numb[0])    # This is the first digit of the numb
        numb1 = int(numb[1])    # This is the second digit of the numb
        list_of_rows = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J')
        seat_row = list_of_rows[numb0]              # This code is to assign the seat 
        seat_number = str(seat_row) + str(numb1)    # row and number to the student

        self.seat_info = Label(self.master, text="Seat Number:", bg="dark blue", fg="grey", width=15).grid(row=7, column=0, pady='1')
        self.seat = Label(self.master, text=seat_number, bg="light blue", width=30)
        self.seat.grid(row=7, column=1, pady='1')   # This displays the user's seat number and row for the movie

        self.back = Button(self.master, font=("Times New Roman", 12), text="Back", fg="white", bg='black',
                           command=self.back).grid(row=8, column=0, pady='1')   # This button returns the user
                                                                                # to the student login page
        self.log_out = Button(self.master, font=("Times New Roman", 12), text="Logout", fg="white", bg='black',
                          command=self.logout).grid(row=8, column=1, pady='1')  # This allows the user 
                                                                                # to sign out of his account
        c.execute('SELECT first, last FROM students WHERE username = ?', (username,))
        both_names = c.fetchone()   # This retrieves the first 
        with conn3:                 # and last name of the user
            c3.execute('INSERT INTO bookings VALUES (?, ?, ?, ?, ?, ?)',    # This line inserts the details of the 
                       (both_names[0], both_names[1], self.datetime1[0],    # booking into the bookings database
                        self.datetime1[1], seat_number, username))
                            
    
class BookingHistory(Booked):
    ''' This class is for the user to be able to view the movie bookings which they
    have made also allowing them to remove the ones which they'd dislike'''
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        # self.background = Label(self.master, image=back_pic)
        # self.background.place(x=0, y=0, relwidth=1, relheight=1)
        self.frame.grid(row=0, column=0)

        self.date = Label(self.master, text='Date', font=("Times New Roman", 15, "bold"), bg="dark blue", fg ="grey", width='15')
        self.date.grid(row=0, column=0)     # These labels are for the headers of each columns and under them you would 
        self.time = Label(self.master, text='Time', font=("Times New Roman", 15, "bold"), bg="dark blue", fg ="grey", width='10')
        self.time.grid(row=0, column=1)     # have rows of movies which have been booked by the user
        self.title = Label(self.master, text='Title', font=("Times New Roman", 15, "bold"), bg="dark blue", fg ="grey", width='33')
        self.title.grid(row=0, column=2)   
        self.seatno = Label(self.master, text='Seat Number', font=("Times New Roman", 15, "bold"), bg="dark blue", fg ="grey", width='15')
        self.seatno.grid(row=0, column=3)  
        self.remove_booking = Label(self.master, text='Remove Booking', font=("Times New Roman", 15, "bold"), bg="dark blue", fg ="grey", width='15')
        self.remove_booking.grid(row=0, column=4)
        c3.execute('''SELECT date, time, seatno FROM bookings WHERE
                    username = ? ORDER BY date='Monday 12/08/19' DESC,
                                                    date='Tuesday 13/08/19' DESC,
                                                    date='Wednesday 14/08/19' DESC,
                                                    date='Thursday 15/08/19' DESC,
                                                    date='Friday 16/08/19' DESC,
                                                    date='Saturday 17/08/19' DESC,
                                                    date='Sunday 18/08/19' DESC,
                                                    time='1pm' DESC,
                                                    time='2pm' DESC,
                                                    time='3pm' DESC,
                                                    time='4pm' DESC,
                                                    time='5pm' DESC,
                                                    time='6pm' DESC,
                                                    time='7pm' DESC,
                                                    time='8pm' DESC,
                                                    time='9pm' DESC,
                                                    time='10pm' DESC''', (username,))
        tempresult = c3.fetchall()
        for i in tempresult:    
            c2.execute('''SELECT title FROM movies WHERE
                        date = ? AND time = ?''', (i[0], i[1]))
            movie_name = c2.fetchone() # This is the title of the movie
            movie_date = Label(self.master, text=i[0], font=("Times New Roman", 12), bg="light blue", width='17')
            movie_date.grid(row=tempresult.index(i) + 1, column=0)
            movie_time = Label(self.master, text=i[1], font=("Times New Roman", 12), bg="light blue", width='10')
            movie_time.grid(row=tempresult.index(i) + 1, column=1)
            movie_title = Label(self.master, text=movie_name[0], font=("Times New Roman", 12), bg="light blue", width='40')
            movie_title.grid(row=tempresult.index(i) + 1, column=2)
            movie_seat_no = Label(self.master, text=i[2], font=("Times New Roman", 12), bg="light blue", width='15')
            movie_seat_no.grid(row=tempresult.index(i) + 1, column=3)
            movie_remove = Button(self.master, text='remove', font=("Times New Roman", 12), bg="light blue", width='15',
                        command=partial(self.remove, i[0], i[1]))   # Partial is used here to allow the function to be 
            movie_remove.grid(row=tempresult.index(i) + 1, column=4)# called with a button without being called automatically
        self.back = Button(self.master, font=("Times New Roman", 12), text="Back", fg="white", bg='black',
                           command=self.back).grid(row=20, column=0)    # This button calls the function 
                                                                        # called back in searchresults class
        self.log = Button(self.master, font=("Times New Roman", 12), text="Logout", fg="white", bg='black',
                          command=self.logout).grid(row=20, column=1)   # This function calls the function
                                                                        # called logout in the student class

    def remove(self, date1, time):      # This function is responsible for removing bookings
        ask_yes = tkinter.messagebox.askyesno('Remove', 'Are you sure you want remove this booking?')
        if ask_yes:
            today_hour = datetime.today().hour - 12     # This gets the hour, day, 
            today_day = date.today().day                # month and year of today
            today_month = date.today().month
            today_year = date.today().year
            new_time = int(time[:-2])
            temp_date = date1.split()
            new_date = int(temp_date[1][:2])
            # The if statement blow checks whether the time of the movie has already passed
            if today_year > 2019 or \
                    today_year == 2019 and today_month > 8 or \
                    today_year == 2019 and today_month == 8 and today_day > new_date or \
                    today_year == 2019 and today_month == 8 and today_day == new_date and today_hour >= new_time:
                tkinter.messagebox.showinfo("---- ERROR ----", "Date and time of showing has passed!", icon="warning")
                # If the time of the movie has already passed then it displays a messagebox and does nothing.
            else:
                with conn3:
                    c3.execute('''DELETE FROM bookings WHERE
                                username = ? AND date = ? AND time = ?''',
                               (username, date1, time))         # If the time has not passed then, it
                                                                # deletes the movie from bookings
                c2.execute('''SELECT booked FROM movies WHERE   
                date = ? AND time = ?''', (date1, time))    # This selects the field called booked in the database movies          
                temp_taken = c2.fetchone()      # fetchone allows me to store the value of booked 
                with conn2:
                    c2.execute('''UPDATE movies SET booked = ?, available = ? WHERE
                    date = ? AND time = ?''', (temp_taken[0] - 1, 100 - (temp_taken[0] - 1), date1, time))
                    # This is to update the movies booked and available values
                tkinter.messagebox.showinfo("---- REMOVED ----", "Film removed from booking history.", icon="info")
                self.newWindow = Toplevel(self.master)
                self.newWindow.geometry('1096x720')
                self.app = BookingHistory(self.newWindow)
                self.master.withdraw()


class Teacher(Student):
    '''Teacher login page'''

    def __init__(self, master):
        super().__init__(master)    # I use supercharge to copy the student 
                                    # login page since they look the same
    def login(self):    # This function is responsible for 
        global username # logging in the teacher to their account
        global password
        
        teacher_username = self.username.get()
        teacher_password = self.password.get()
        lines = iter([line.rstrip('\n') for line in open('Teachers.txt', 'r')])
        # I use the text document called Teachers to store the teacher's account information
        for i in lines: 
            j = i.split(': ')   # This splits the user's username and password
            if teacher_username == j[0] and teacher_password == j[1]:
                self.newWindow = Toplevel(self.master)
                self.newWindow.geometry('1096x720')
                self.app = TeacherMain(self.newWindow)
                self.master.withdraw()
                tkinter.messagebox.showinfo("---- SUCCESS ----", "You Have Now Logged In.", icon="info")
                break
        else:
            tkinter.messagebox.showinfo("---- ERROR ----", "Incorrect login! Please try again", icon="warning")


class TeacherMain(Teacher):
    '''Teacher main menu page. This page allows the teacher to add films and see films which are being shown'''

    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        # self.background = Label(self.master, image=back_pic)
        # self.background.place(x=0, y=0, relwidth=1, relheight=1)
        self.frame.pack()
        self.showings = Button(self.master, font=("Times New Roman", 16), text="See list of film showings", bg="light blue",
                               command=self.See_list).pack(pady='5')    # This button calls for the function see_list
        self.add = Button(self.master, font=("Times New Roman", 16), text="Add film showings", bg="light blue",
                          command=self.Add_film_showings).pack(pady='5')    # This button calls for the function Add_film_showings
        self.log = Button(self.master, font=("Times New Roman", 12), text="Logout", fg="white", bg='black',
                          command=self.logout).pack(pady='5')

    def logout(self):   # This functions allows the user to sign out
        ask_yes = tkinter.messagebox.askyesno('Logout', 'Are you sure you want to log out?')
        if ask_yes:
            self.newWindow = Toplevel(self.master)
            self.newWindow.geometry('1096x720')
            self.app = MainPage(self.newWindow)
            self.master.withdraw()

    def See_list(self): 
        self.newWindow = Toplevel(self.master)
        self.newWindow.geometry('1096x720')
        self.app = Showings(self.newWindow)
        self.master.withdraw()

    def Add_film_showings(self):
        self.newWindow = Toplevel(self.master)
        self.newWindow.geometry('1096x720')
        self.app = AddShowings(self.newWindow)
        self.master.withdraw()
    


class Showings(TeacherMain):
    '''Shows a list of times and dates that have a film showing. The dates range from Monday 12th - Friday 18th
    August 2019, and times range from 1-11pm (with the last showing at 10pm). The shows are for exactly
    one hour'''

    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        # self.background = Label(self.master, image=back_pic)
        # self.background.place(x=0, y=0, relwidth=1, relheight=1)
        self.frame.grid(row=0, column=0)
        self.date = Label(self.master, text='Date', font=("Times New Roman", 16, "bold"), bg="dark blue", fg="grey", width=8)
        self.date.grid(row=0, column=1, pady='1')   # These are the headers at the top of the page for each 
        self.time = Label(self.master, text='Time', font=("Times New Roman", 16, "bold"), bg="dark blue", fg="grey", width=6)
        self.time.grid(row=0, column=2, pady='1')   # of the columns and below this are rows of films showings
        self.title = Label(self.master, text='Title', font=("Times New Roman", 16, "bold"), bg="dark blue", fg="grey", width=18)
        self.title.grid(row=0, column=3, pady='1')
        self.description = Label(self.master, text='Description', font=("Times New Roman", 16, "bold"), bg="dark blue", fg="grey", width=32)
        self.description.grid(row=0, column=4, pady='1')                                                                                                                                                                                                                
        self.booked = Label(self.master, text='Booked', font=("Times New Roman", 16, "bold"), bg="dark blue", fg="grey",width=8)
        self.booked.grid(row=0, column=5, pady='1')
        self.available = Label(self.master, text='Available', font=("Times New Roman", 16, "bold"), bg="dark blue", fg = "grey", width=8)
        self.available.grid(row=0, column=6, pady='1')
        self.remove_movie = Label(self.master, text='Remove', font=("Times New Roman", 16, "bold"), bg="dark blue", fg = "grey", width=8)
        self.remove_movie.grid(row=0, column=7, pady='1')
        c2.execute('''SELECT * FROM movies ORDER BY date='Monday 12/08/19' DESC, date='Tuesday 13/08/19' DESC, date='Wednesday 14/08/19' DESC,
                                                    date='Thursday 15/08/19' DESC, date='Friday 16/08/19' DESC, date='Saturday 17/08/19' DESC,
                                                    date='Sunday 18/08/19' DESC,
                                                    time='1pm' DESC, time='2pm' DESC, time='3pm' DESC, time='4pm' DESC, time='5pm' DESC,
                                                    time='6pm' DESC, time='7pm' DESC, time='8pm' DESC, time='9pm' DESC, time='10pm' DESC''')
        output = c2.fetchall()  # This retrieves all the field records in the movie database 
        widths = (15, 6, 40, 60, 8, 8, 12)  # This is a list of numbers for the widths of the labels
        for i in output:    # This loops through all the movies and its informations stored in output
            for j in i:     # This loops the informations of the movie
                info_labels = Label(self.master, text=j, font=("Times New Roman", 6), bg= "light blue", width=widths[i.index(j)])
                info_labels.grid(row=output.index(i) + 1, column=i.index(j) + 1, pady='1')
            self.date_movie = i[0]  # This retrieves the date and of each of the movie which is
            self.time_movie = i[1]  # stored and will get passed down later via the delete_button       
            delete_button = Button(self.master, text='Remove',
                                   command=partial(self.delete_movie, self.date_movie, self.time_movie), font=("Times New Roman", 7), bg="light blue", width=8)
                                    # Using a partial here allows a function to be called in a button 
                                    # with a parameter without the function being called automatically            
            delete_button.grid(row=output.index(i) + 1, column=7, pady='1')
        self.back = Button(self.master, font=("Times New Roman", 12), text="Back", bg="black", fg="white",
                           command=self.back).grid(row=35, column=1, pady='1')
        self.log = Button(self.master, font=("Times New Roman", 12), text="Logout", bg="black", fg="white",
                          command=self.logout).grid(row=35, column=2, pady='1')

    def back(self):     # Function returns the user to the teacher's home page
        self.newWindow = Toplevel(self.master)
        self.newWindow.geometry('1096x720')
        self.app = TeacherMain(self.newWindow)
        self.master.withdraw()

    def delete_movie(self, date_movie, time_movie):    # This function is responsible for deleting a movie
        ask_yes = tkinter.messagebox.askyesno("Remove", "Are you sure you want to delete this movie?")
        # A message box displayed to ask the teacher if he is sure of this change
        if ask_yes: 
            self.date1 = date_movie
            self.time = time_movie
            with conn2: # Using with allows me to access the database and change it permanently
                c2.execute('''DELETE FROM movies WHERE
                date = ? AND time =?''', (self.date1, self.time))                
            self.newWindow = Toplevel(self.master)
            self.newWindow.geometry('1096x720')
            self.app = TeacherMain(self.newWindow)
            self.master.withdraw()
        
                            
class AddShowings(Showings):
    ''' This class is responsible for displaying a page and it also allows the teacher to
    add movies to the movies database manually '''
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        # self.background = Label(self.master, image=back_pic)
        # self.background.place(x=0, y=0, relwidth=1, relheight=1)
        self.frame.grid(row=0, column=0)

        self.title = Label(self.master, text="Please add a new showing below",
                           font=("Times New Roman", 16, "bold"), bg="dark blue", fg="grey", width=45)
        self.title.grid(row=0, column=0, pady='5', columnspan=2)
        # This title is a guide to the teacher advising him what to do in this page
        self.date = Label(self.master, text="Date:", bg="light blue", width=15).grid(row=1, column=0, pady='3')
        self.defdate = StringVar(self.master)
        self.defdate.set("Monday 12/08/19")  # This if the default value for the option menu
        self.datelist = OptionMenu(master, self.defdate, "Monday 12/08/19", "Tuesday 13/08/19", "Wednesday 14/08/19",
                                   "Thursday 15/08/19", "Friday 16/08/19", "Saturday 17/08/19", "Sunday 18/08/19")
                                    # This option menu allows the teacher to choose the date of the movie showing
        self.datelist.grid(row=1, column=1, pady='3')

        self.time = Label(self.master, text="Time:", bg="light blue", width=15).grid(row=2, column=0, pady='3')
        self.deftime = StringVar(self.master)
        self.deftime.set("1pm")  # This is the default value for the option menu
        self.timelist = OptionMenu(master, self.deftime, "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm", "8pm",
                                   "9pm", "10pm")
                                    # This option menu allows the user to choose what time the movie will be showing
        self.timelist.grid(row=2, column=1, pady='3')

        self.movie_title = Label(self.master, text="Title:", bg="light blue", width=15).grid(row=3, column=0, pady='3')
        self.title_entry = Entry(self.master, width='45')   # This is the entry field where the teacher
        self.title_entry.grid(row=3, column=1, pady='3')    # is required to enter the movie's title

        self.desc = Label(self.master, text="Description:", bg="light blue", width=15).grid(row=4, column=0, pady='3')
        self.description = Entry(self.master, width='45')
        self.description.grid(row=4, column=1, columnspan=4, pady='3')
        self.add_film = Button(self.master, font=("Times New Roman", 8, "bold"), text="Add Film Showing", bg= "dark blue", fg="grey",
                               command=self.add_new)     # This button calls for the function addnew
        self.add_film.grid(row=5, columnspan=5, pady='3')
        
        self.back = Button(self.master, font=("Times New Roman", 12), text="Back", fg="white", bg='black',
                           command=self.back).grid(row=11, column=0, pady='3')
        self.log = Button(self.master, font=("Times New Roman", 12), text="Logout", fg="white", bg='black',
                          command=self.logout).grid(row=11, column=1, pady='3')

    def add_new(self):   # This function is responsible for adding a movie in the database
        ask_yes = tkinter.messagebox.askyesno('Logout', 'Confirm new showing?')
        if ask_yes:     # If the user clicks yes to the message box the condition would be met
            new_date = self.defdate.get()
            new_time = self.deftime.get()   # Retrieves the movie's information which was inputted in
            new_title = self.title_entry.get()
            new_description = self.description.get()
            c2.execute("""SELECT * FROM movies WHERE
                        date = ? AND time = ?""", (new_date, new_time))
            if not new_date or not new_time or not new_title or not new_description:
                tkinter.messagebox.showinfo("---- ERROR ----", "Please complete all required fields.",
                                            icon="warning")
            else:
                if not c2.fetchall():
                    with conn2:
                        c2.execute("""INSERT INTO movies VALUES (?, ?, ?, ?, ?, ?)""", (
                            new_date, new_time, new_title, new_description, 0, 100))
                        # Uses the information which was inputed by the teacher to
                        # insert into the database as a new field record
                        tkinter.messagebox.showinfo("---- SUCCESSFUL ----",
                                                    "Showing successfully added to list of showings!",
                                                    icon="info")
                else:
                    tkinter.messagebox.showinfo("---- ERROR ----", "There is already a showing at this time!",
                                                icon="warning")

def Students_Database_Initialiser():
    '''Initialises the database for the students'''
    global conn
    conn = sqlite3.connect('students.db')
    global c
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students(
                first text,
                last text,
                email text,
                age integer,
                username text,
                password text
                )''')

    def create():
        student = iter([line.rstrip('\n') for line in open('students.txt', 'r')])
        for i in student:
            j = i.split(': ')
            k = j[0].split('_')
            c.execute('INSERT INTO students VALUES (?, ?, ?, ?, ?, ?)',
                      (k[0], k[1], str(j[0] + '@gmail.com'), randrange(10, 60), j[0], j[1]))

    # create()  # Uncomment this line if you want to create the database
                # using a document full of student's information from scratch
    conn.commit()


def Films_Database_Initialiser():
    '''Initialises the database for all the film showings'''
    
    global conn2
    conn2 = sqlite3.connect('movies.db')
    global c2
    c2 = conn2.cursor()
    c2.execute('''CREATE TABLE IF NOT EXISTS movies(
                date text,
                time text,
                title text,
                description text,
                booked integer,
                available integer
                )''')
    
    def create():
        mov = iter([line.rstrip('\n') for line in open('MOVIES.txt', 'r')])
        for i in mov:
            j = i.split(': ')
            c2.execute('INSERT INTO movies VALUES (?, ?, ?, ?, ?, ?)', (j[0], j[1], j[4], j[5], j[2], j[3]))

    #create() # Uncomment this line if you want to create the databases again from scratch
    conn2.commit()


def Bookings_Database_Initialiser():
    '''Initlaises the database for film bookings'''
    global conn3
    conn3 = sqlite3.connect('bookings.db')
    global c3
    c3 = conn3.cursor()
    c3.execute('''CREATE TABLE IF NOT EXISTS bookings(
                    first text,
                    last text,
                    date text,
                    time text,
                    seatno text,
                    username text
                    )''')
    conn3.commit()


def main():
    window = Tk()                           # This is the function which starts
    window.title("Adnan's Cinema")          # the whole tkinter window and 
    window.geometry('1096x720')             # customises the window
    
    # image = Image.open("Background.png")    # This is the background image of the window which 
                                            # will be retrieved from the background file
                                            
    Students_Database_Initialiser()     # These 3 functions are being called and                          
    Films_Database_Initialiser()        # the job of them is to create all the                            
    Bookings_Database_Initialiser()     # databases needed for this program                                                                                                    
    # global back_pic
    # image = Label(window, image=back_pic)
    # image.place(x=0, y=0, relwidth=1, relheight=1)
    app = MainPage(window)
    window.mainloop()                           

main()  # This calls the function above which starts the program