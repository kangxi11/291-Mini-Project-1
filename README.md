# 291-Mini-Project-1
repository for the mini-project-1 between group members

You are given the following relational schema.

persons(fname, lname, bdate, bplace, address, phone)
births(regno, fname, lname, regdate, regplace, gender, f_fname, f_lname, m_fname, m_lname)
marriages (regno, regdate, regplace, p1_fname, p1_lname, p2_fname, p2_lname)
vehicles(vin,make,model,year,color)
registrations(regno, regdate, expiry, plate, vin, fname, lname)
tickets(tno,regno,fine,violation,vdate)
demeritNotices(ddate, fname, lname, points, desc)
payments(tno, pdate, amount)
users(uid, pwd, utype, fname, lname, city)


These tables are derived from the specification of Assignment 1 and are identical to those in Assignment 2 except the tables payments and users, which are new. The table payments will keep all payments made toward tickets and the table users will list the users of the system. A ticket can be paid in one or more payments. The column utype in users can take one of the two values: 'a' for agents and 'o' for officers, and the column city in the same table gives the location of the registry agent or the traffic officer. The SQL commands to create the tables of the system are given here (right click to save as a file). Use the given schema in your project and do not change any table/column names.

Login Screen
The first screen of your system should provide options for users to login. Each user of the system should be able to login using a valid user id and password, denoted with uid and pwd in table users. After a successful login, users should be able to perform the subsequent operations (possibly chosen from a menu) as discussed next. The operations are different for each user type.

Users should be able to logout and there must be also an option to exit the program.

System Functionalities
Registry agents should be able to perform all of the following tasks.

Register a birth.The agent should be able to register a birth by providing the first name, the last name, the gender, the birth date, the birth place of the newborn, as well as the first and last names of the parents. The registration date is set to the day of registration (today's date) and the registration place is set to the city of the user. The system should automatically assign a unique registration number to the birth record. The address and the phone of the newborn are set to those of the mother. If any of the parents is not in the database, the system should get information about the parent including first name, last name, birth date, birth place, address and phone. For each parent, any column other than the first name and last name can be null if it is not provided.
Register a marriage.The user should be able to provide the names of the partners and the system should assign the registration date and place and a unique registration number as discussed in registering a birth. If any of the partners is not found in the database, the system should get information about the partner including first name, last name, birth date, birth place, address and phone. For each partner, any column other than the first name and last name can be null if it is not provided.
Renew a vehicle registration.The user should be able to provide an existing registration number and renew the registration. The system should set the new expiry date to one year from today's date if the current registration either has expired or expires today. Otherwise, the system should set the new expiry to one year after the current expiry date.
Process a bill of sale.The user should be able to record a bill of sale by providing the vin of a car, the name of the current owner, the name of the new owner, and a plate number for the new registration. If the name of the current owner (that is provided) does not match the name of the most recent owner of the car in the system, the transfer cannot be made. When the transfer can be made, the expiry date of the current registration is set to today's date and a new registration under the new owner's name is recorded with the registration date and the expiry date set by the system to today's date and a year after today's date respectively. Also a unique registration number should be assigned by the system to the new registration. The vin will be copied from the current registration to the new one.
Process a payment.The user should be able to record a payment by entering a valid ticket number and an amount. The payment date is automatically set to the day of the payment (today's date). A ticket can be paid in multiple payments but the sum of those payments cannot exceed the fine amount of the ticket.
Get a driver abstract.The user should be able to enter a first name and a last name and get a driver abstract, which includes the number of tickets, the number of demerit notices, the total number of demerit points received both within the past two years and within the lifetime. The user should be given the option to see the tickets ordered from the latest to the oldest. For each ticket, you will report the ticket number, the violation date, the violation description, the fine, the registration number and the make and model of the car for which the ticket is issued. If there are more than 5 tickets, at most 5 tickets will be shown at a time, and the user can select to see more.
Traffic officers should be able to perform all of the following tasks.

Issue a ticket.The user should be able to provide a registration number and see the person name that is listed in the registration and the make, model, year and color of the car registered. Then the user should be able to proceed and ticket the registration by providing a violation date, a violation text and a fine amount. A unique ticket number should be assigned automatically and the ticket should be recorded. The violation date should be set to today's date if it is not provided.
Find a car owner.The user should be able to look for the owner of a car by providing one or more of make, model, year, color, and plate. The system should find and return all matches. If there are more than 4 matches, you will show only the make, model, year, color, and the plate of the matching cars and let the user select one. When there are less than 4 matches or when a car is selected from a list shown earlier, for each match, the make, model, year, color, and the plate of the matching car will be shown as well as the latest registration date, the expiry date, and the name of the person listed in the latest registration record.
String matching. Except the password which is case-sensitive, all other string matches (include user id, name, etc.) are case-insensitive. This means edmonton will match Edmonton, EDMONTON, edmontoN and edmonton, and you cannot make any assumption on the case of the strings in the database. The database can have strings in uppercase, lowercase or any mixed format.

Error checking. Every good programmer should do some basic error checking to make sure the data entered is correct. We cannot say how much error checking you should or should not do, or detail out all possible checkings. However, we can say that we won't be trying to break down your system but your system also should not break down when the user makes a mistake.

Groups of size 3 must counter SQL injection attacks and make the password non-visible at the time of typing.
