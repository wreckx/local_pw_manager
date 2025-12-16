from cryptography.fernet import Fernet

class SymmetricEncryption:
    
    def __init__(self):
        self.key = None
        
    def create_key(self, path):
        self.key = Fernet.generate_key()
        
        with open(path, 'wb') as file:
            file.write(self.key)
            
    def load_key(self, path):
        try:
            with open(path, 'rb') as file:
                self.key = file.read()
        except FileNotFoundError:
            print(f"Key file not found at {path}")
            
    def encrypt_passwd(self, passwd:str):
        if self.key is not None:
            return Fernet(self.key).encrypt(passwd.encode())
        else:
            print("Cannot encrpyt without a key")
    
    def decrypt_passwd(self, passwd:str):
        if self.key is not None:
            return Fernet(self.key).decrypt(passwd.encode()).decode()
        else:
            print("Cannot decrpyt without a key")