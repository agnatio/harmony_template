# this module only generates the secret key then keeps it.
# key generation is commented out

from cryptography.fernet import Fernet

key = Fernet.generate_key()
print(key)


secret_key = b"xHum_1vjvvWBmthIVl8JAS9u9esZqvUHsxkzTYZnd5I="
