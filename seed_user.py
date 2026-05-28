import random
import sys
from datetime import datetime

sys.path.insert(0, "database")
from db import get_db
from werkzeug.security import generate_password_hash

FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Wasif", "Rohan", "Karthik", "Imran",
    "Saurabh", "Neha", "Priya", "Ananya", "Ishita", "Meera", "Fatima",
    "Rahul", "Sneha", "Arjun", "Divya", "Kabir", "Pooja",
]
LAST_NAMES = [
    "Sharma", "Verma", "Abbas", "Iyer", "Reddy", "Nair", "Khan",
    "Gupta", "Patel", "Mehta", "Joshi", "Das", "Rao", "Banerjee",
    "Kulkarni", "Chowdhury", "Pillai", "Sinha", "Bose", "Naidu",
]


def generate_user():
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    name = f"{first} {last}"
    suffix = random.randint(10, 999)
    email = f"{first.lower()}.{last.lower()}{suffix}@gmail.com"
    return name, email


def email_exists(conn, email):
    row = conn.execute("SELECT 1 FROM users WHERE email = ?", (email,)).fetchone()
    return row is not None


def main():
    conn = get_db()
    try:
        name, email = generate_user()
        while email_exists(conn, email):
            name, email = generate_user()

        password_hash = generate_password_hash("dummypassword")
        created_at = datetime.now().isoformat(sep=" ", timespec="seconds")

        conn.execute(
            "INSERT INTO users (name, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
            (name, email, password_hash, created_at),
        )
        conn.commit()

        print("User created successfully!")
        print(f"  Name:       {name}")
        print(f"  Email:      {email}")
        print(f"  Created at: {created_at}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
