# Personal Password Manager
## Personal Project

This is a GUI personal password manager that uses python as base and stores password in an offline database located in your local drive.
The manager should do the following:
+ Prompt to create a master password on first time use.
    - Hash the masterpassword using bcrypt and store it in the database.
    - On subsequent use, program should prompt for the password to access the manager itself.
+ Have a search feature to search for accounts using username, email, or site name.
+ Add, remove, or edit entries from a button and store data in the databae.
+ Allow the ability to generate a random password.
+ Passwords are encrypted and hidden and must reenter the master password to access it.
