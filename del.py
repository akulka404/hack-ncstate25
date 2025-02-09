import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Delete all users from the database
cursor.execute("DELETE FROM users")
conn.commit()

# Confirm deletion
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()

if not users:
    print("✅ All users have been deleted successfully!")
else:
    print("⚠ Some users still exist.")

# Close the connection
conn.close()
