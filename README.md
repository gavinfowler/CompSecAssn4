# Computer Security Assn 4

Assignment 4: Secure authentication

Run with:

```sh
pip3 install -r requirements.txt
python3 app.py
```

## TODO:

### Task 1

- [ ] Create list of dictionary words (30)
- [ ] Create list of dictionary word replacements
- [ ] Create UI for Task 1

### Task 2

- [ ] Create UI form to accept input
- [ ] Create backend to accept data from input
- [ ] Generate list of popular passwords from form

### Task 3A

- [ ] Create UI for account creation (include form from task 2)
- [ ] Create backend for account creation

### Task 3B

- [ ] Generate and save salt

```python
import secrets
random_string = secrets.token_hex(8))
```

- [ ] Salt the password and hash the password

```python
import hashlib
hashlib.sha224(b"Text").hexdigest()
```

- [ ] Save the salted and hashed password to file

### Task 3C

- [ ] Create UI for login
- [ ] Create backend for login, using info from task 1 and 2
- [ ] Implement UI lockout
