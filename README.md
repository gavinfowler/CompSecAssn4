# Computer Security Assn 4

Assignment 4: Secure authentication

Uses the python Black linter.

Run with:

```sh
pip3 install -r requirements.txt
python3 app.py
```

## TODO:

### Task 1

- [x] Create list of dictionary words (30)
- [x] Create list of dictionary word replacements
- [x] Create UI for Task 1
- [x] Create Backend for Task 1

### Task 2

- [x] Create UI form to accept input
- [x] Create backend to accept data from input
- [x] Generate list of popular passwords from form

### Task 3A

- [x] Create UI for account creation (include form from task 2)
- [x] Create backend for account creation

### Task 3B

- [x] Generate and save salt

```python
import secrets
random_string = secrets.token_hex(8))
```

- [x] Salt the password and hash the password

```python
import hashlib
hashlib.sha224(b"Text").hexdigest()
```

- [x] Save the salted and hashed password to file

### Task 3C

- [x] Create UI for login
- [x] Create backend for login, using info from task 1 and 2
- [x] Implement UI lockout
