import argparse
from argon2 import PasswordHasher

def generate_hash(password):
    ph = PasswordHasher()
    return ph.hash(password)

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Generate an Argon2 hash from a password")
    parser.add_argument("password", help="The password to hash")
    
    args = parser.parse_args()
    
    # Generate hash
    hashed_password = generate_hash(args.password)
    
    # Print the result
    print(hashed_password)

if __name__ == "__main__":
    main()