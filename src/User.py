import os
from cryptography.fernet import Fernet
import json

class User:

    def __init__(self):
        self.user_id = None
        self.password = None

    def createUser(self):
        self.user_id = str(input('Enter Linkedin userid: '))
        self.password = str(input('Enter password: '))

    def loadUser(self):
        with open('./src/.res/user.json', 'r') as file:
            login = json.load(file)
            key = login['key'].encode()
            cs = Fernet(key)
            self.user_id = login['user_id']
            self.password = str(cs.decrypt(login['password'].encode()).decode())

    def saveUser(self):
        save = input('Save User on device? (Y): ')
        if save.strip().lower() in ['y','yes']:
            key = Fernet.generate_key()
            cs = Fernet(key)
            cs_text = cs.encrypt(self.password.encode())
            dict = {
                "user_id": self.user_id,
                "password": cs_text.decode(),
                "key": key.decode()
            }
            with open('./src/.res/user.json', 'w') as file:
                json.dump(dict, file)

    def login(self):
        last = 'n'
        if os.path.isfile('./src/.res/user.json'):
            last = input('Login with last saved user? (Y): ')
        if last.strip().lower() in ['y', 'yes']:
            self.loadUser()
        elif last.strip().lower() in ['n', 'no']:
            self.createUser()
            self.saveUser()
        return self.user_id, self.password