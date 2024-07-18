from cryptography.fernet import Fernet

# Generate a key for encryption
key = Fernet.generate_key()

# Save the key to a file for decryption use in the program
with open('secret.key', 'wb') as key_file:
    key_file.write(key)

print("Kunci enkripsi telah dihasilkan dan disimpan sebagai 'secret.key'.")
