# Personal Password Manager

## Personal Project

This is a GUI personal password manager that uses python as base and stores password in an offline database located in your local drive.
Passwords and master password are stored in a local SQLite database and accessed by the program.

The manager offers the following features:

- Prompt to create a master password on first time use.
  - Master password is hashed using brcrypt and stored in the database
  - Program prompts for the master password to access the password manager on subsequent use.
- Search feature allows to search for records using the stored website name, username, or email address as keywords.
- New records can be added and old records can be modified or delete using the Add, Edit, and Delete buttons respectively
- Allow random password generation if desired for each added or modified record.
- Passwords are encrypted before storage and needs master password to access.
  - Passwords are symmetrically encrypted using AES-128 encryption and fingerprinted by a program generated key.
  - Program generated key is used by authentication hashed using SHA-256
  - Encrypted passwords are stored in the database and needs master password authentication to access and copy.
  - Passwords are automatically copied to the clipboard upon retrieval
