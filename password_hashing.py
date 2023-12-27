import bcrypt

def hash_password(plaintext_password):
    # Hash the plaintext password using bcrypt
    hashed_password = bcrypt.hashpw(plaintext_password.encode('utf-8'), bcrypt.gensalt())
    

    return hashed_password


# Store hashed_password in the database
def verify_password(entered_password, stored_hashed_password):
    # Check if entered password matches the stored hashed password
    return bcrypt.checkpw(entered_password.encode('utf-8'), stored_hashed_password)


