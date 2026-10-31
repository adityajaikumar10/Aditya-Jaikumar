Project: Vehicle Rental System (Python & SQLite)
Role: Admin & Customer Management System

REQUIREMENTS:
- Python 3.x installed

HOW TO RUN THE PROJECT:
1. Ensure both the Python script (`vehicle_rental_system.py`) and the database file (`vehicle_rental.db`) are in the same folder.
2. Open your terminal or command prompt.
3. Navigate to the project folder.
4. Run the program using the command: python vehicle_rental_system.py (or python3 vehicle_rental_system.py on Mac/Linux).

TESTING THE SYSTEM (SAMPLE RECORDS INCLUDED):
- The attached `vehicle_rental.db` file comes pre-loaded with sample data.
- To test Admin privileges (Create, Update, Delete vehicles), log in with the Admin account you created.
- To test Customer privileges (Rentals, View History), log in with a Customer account.
- Or, use the "Register" option on the main menu to create fresh accounts and test the database constraints!


Created Admin login Credentials
User name: Aditya
Password : Aditya


Created User login Credentials

1
User name:adi
Password :123
2
User name:Messi
Password :10
3
User name:Ronaldo
Password :7
4
User name:Kane
Password :0


=====================================================================================================================================================================================
=====================================================================================================================================================================================
=====================================================================================================================================================================================


PYTHON CODE:-

import sqlite3
import sys

# The file where all our data will be stored.
DATABASE_FILE = "vehicle_rental.db"


# ==========================================
# 1. DATABASE SETUP & CONNECTION
# ==========================================
def connect_to_database():
    """Opens a connection to the database and turns on foreign key rules."""
    try:
        connection = sqlite3.connect(DATABASE_FILE)
        # We turn on foreign keys so the database knows how tables are linked together.
        # This stops us from doing things like renting out a car that doesn't exist.
        connection.execute("PRAGMA foreign_keys = ON;")
        return connection
    except sqlite3.Error as error_message:
        print(f"\nOops! We couldn't connect to the database. Reason: {error_message}")
        sys.exit(1)  # Stop the program safely if the database fails


def setup_database_tables():
    """Creates the 3 main tables if this is the first time running the app."""
    connection = connect_to_database()
    try:
        cursor = connection.cursor()

        # Table 1: Users (Stores both Admins and Customers)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('Admin', 'Customer'))
            )
        """)

        # Table 2: Vehicles (Stores the cars available for rent)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehicles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brand TEXT NOT NULL,
                model TEXT NOT NULL,
                daily_rate REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'Available' CHECK(status IN ('Available', 'Rented'))
            )
        """)

        # Table 3: Rentals (The bridge between Users and Vehicles)
        # Using ON DELETE CASCADE means if a user is deleted, their rental history is also cleaned up.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rentals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                vehicle_id INTEGER NOT NULL,
                days INTEGER NOT NULL,
                total_cost REAL NOT NULL,
                rental_status TEXT NOT NULL DEFAULT 'Active' CHECK(rental_status IN ('Active', 'Returned')),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE
            )
        """)
        connection.commit()  # Save the changes
    except sqlite3.Error as error_message:
        print(f"\nOops! Something went wrong while setting up the database: {error_message}")
    finally:
        # Always remember to close the door when you leave!
        connection.close()


# ==========================================
# 2. HELPER FUNCTIONS (To handle user mistakes nicely)
# ==========================================
def ask_for_text(prompt_message):
    """Keeps asking until the user types something (prevents empty inputs)."""
    while True:
        user_input = input(prompt_message).strip()
        if user_input:  # If the string is not empty
            return user_input
        print("-> Please type something. This field cannot be empty.")


def ask_for_money(prompt_message):
    """Makes sure the user types a valid price (a positive decimal number)."""
    while True:
        try:
            user_input = float(input(prompt_message).strip())
            if user_input > 0:
                return user_input
            print("-> Please enter a number greater than zero.")
        except ValueError:
            print("-> That doesn't look like a valid number. Try again.")


def ask_for_whole_number(prompt_message):
    """Makes sure the user types a valid ID or number of days (a positive whole number)."""
    while True:
        try:
            user_input = int(input(prompt_message).strip())
            if user_input > 0:
                return user_input
            print("-> Please enter a whole number greater than zero.")
        except ValueError:
            print("-> That doesn't look like a whole number. Try again.")


# ==========================================
# 3. USER ACCOUNTS (Registration & Login)
# ==========================================
def register_new_user():
    """Lets a new person sign up and pick whether they are a Customer or Admin."""
    print("\n--- CREATE A NEW ACCOUNT ---")
    new_username = ask_for_text("Pick a username: ")
    new_password = ask_for_text("Pick a password: ")

    print("\nWhat type of account is this?")
    print("1. Customer (Can rent cars)")
    print("2. Admin (Can manage the fleet)")

    role_choice = ask_for_text("Enter 1 or 2: ")
    if role_choice == "2":
        assigned_role = "Admin"
    else:
        assigned_role = "Customer"

    connection = connect_to_database()
    try:
        cursor = connection.cursor()
        # Save the new user to the database
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (new_username, new_password, assigned_role)
        )
        connection.commit()
        print(f"\nAwesome! '{new_username}' is now registered as a {assigned_role}.")
    except sqlite3.IntegrityError:
        # This specific error happens because we set username to be UNIQUE in the database
        print(f"\nUh oh! The username '{new_username}' is already taken. Try another one.")
    except sqlite3.Error as error_message:
        print(f"\nDatabase error: {error_message}")
    finally:
        connection.close()


def log_in_user():
    """Checks the username and password and returns the user's details if they match."""
    print("\n--- LOG IN ---")
    username = ask_for_text("Username: ")
    password = ask_for_text("Password: ")

    connection = connect_to_database()
    try:
        cursor = connection.cursor()
        # Look for a match in the database
        cursor.execute(
            "SELECT id, username, role FROM users WHERE username=? AND password=?",
            (username, password)
        )
        found_user = cursor.fetchone()  # Fetch the first matching row

        if found_user:
            print(f"\nWelcome back, {found_user[1]}!")
            # Package the user data nicely into a dictionary so it's easy to use later
            return {
                "id": found_user[0],
                "username": found_user[1],
                "role": found_user[2]
            }
        else:
            print("\nHmm, we couldn't find an account with that username and password.")
            return None
    except sqlite3.Error as error_message:
        print(f"\nDatabase error: {error_message}")
        return None
    finally:
        connection.close()


# ==========================================
# 4. ADMIN TASKS (Manage the fleet)
# ==========================================
def admin_add_new_vehicle():
    """Lets an admin add a brand new car to the system."""
    print("\n--- ADD A NEW VEHICLE ---")
    brand = ask_for_text("Vehicle Brand (e.g., Toyota): ")
    model = ask_for_text("Vehicle Model (e.g., Camry): ")
    daily_rate = ask_for_money("Daily Rental Rate (e.g., 45.50): $")

    connection = connect_to_database()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO vehicles (brand, model, daily_rate) VALUES (?, ?, ?)",
            (brand, model, daily_rate)
        )
        connection.commit()
        print("\nSuccess! The new vehicle has been added to the fleet.")
    except sqlite3.Error as error_message:
        print(f"\nDatabase error: {error_message}")
    finally:
        connection.close()


def show_all_vehicles():
    """Prints out a list of all vehicles. Both Admins and Customers can use this."""
    connection = connect_to_database()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM vehicles")
        all_vehicles = cursor.fetchall()  # Get every single row

        print("\n--- OUR VEHICLE FLEET ---")
        if not all_vehicles:
            print("No vehicles are currently in the system.")
            return

        for vehicle in all_vehicles:
            vehicle_id = vehicle[0]
            brand = vehicle[1]
            model = vehicle[2]
            rate = vehicle[3]
            status = vehicle[4]

            print(f"ID: {vehicle_id} | {brand} {model} | Rate: ${rate:.2f}/day | Status: {status}")
    except sqlite3.Error as error_message:
        print(f"\nDatabase error: {error_message}")
    finally:
        connection.close()


def admin_change_vehicle_price():
    """Lets an admin change how much a vehicle costs per day."""
    show_all_vehicles()
    print("\n--- UPDATE VEHICLE PRICE ---")
    target_id = ask_for_whole_number("Which Vehicle ID do you want to update?: ")
    new_price = ask_for_money("What is the new daily rate?: $")

    connection = connect_to_database()
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE vehicles SET daily_rate = ? WHERE id = ?", (new_price, target_id))

        # rowcount tells us how many rows were actually changed
        if cursor.rowcount > 0:
            connection.commit()
            print("\nSuccess! The vehicle's price has been updated.")
        else:
            print(f"\nWe couldn't find a vehicle with ID {target_id}.")
    except sqlite3.Error as error_message:
        print(f"\nDatabase error: {error_message}")
    finally:
        connection.close()


def admin_remove_vehicle():
    """Lets an admin permanently delete a vehicle."""
    show_all_vehicles()
    print("\n--- DELETE A VEHICLE ---")
    target_id = ask_for_whole_number("Which Vehicle ID do you want to delete?: ")

    connection = connect_to_database()
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM vehicles WHERE id = ?", (target_id,))

        if cursor.rowcount > 0:
            connection.commit()
            print("\nSuccess! The vehicle has been removed from the fleet.")
        else:
            print(f"\nWe couldn't find a vehicle with ID {target_id}.")
    except sqlite3.Error as error_message:
        print(f"\nDatabase error: {error_message}")
    finally:
        connection.close()


# ==========================================
# 5. CUSTOMER TASKS (Renting Cars)
# ==========================================
def rent_a_car(current_user_id):
    """Handles the process of a customer renting a specific vehicle."""
    show_all_vehicles()
    print("\n--- RENT A VEHICLE ---")
    chosen_vehicle_id = ask_for_whole_number("Enter the ID of the vehicle you want to rent: ")
    rental_days = ask_for_whole_number("How many days do you need it for?: ")

    connection = connect_to_database()
    try:
        cursor = connection.cursor()

        # First, let's check if the vehicle exists and if it's available
        cursor.execute("SELECT daily_rate, status FROM vehicles WHERE id = ?", (chosen_vehicle_id,))
        vehicle = cursor.fetchone()

        if vehicle is None:
            print("\nSorry, that Vehicle ID doesn't exist.")
            return

        vehicle_price_per_day = vehicle[0]
        vehicle_status = vehicle[1]

        if vehicle_status == 'Rented':
            print("\nSorry, that vehicle is already checked out by someone else!")
            return

        # Calculate the bill
        total_bill = vehicle_price_per_day * rental_days

        # Step 1: Create a record of the rental
        cursor.execute(
            "INSERT INTO rentals (user_id, vehicle_id, days, total_cost) VALUES (?, ?, ?, ?)",
            (current_user_id, chosen_vehicle_id, rental_days, total_bill)
        )
        # Step 2: Mark the vehicle as unavailable so no one else can rent it
        cursor.execute(
            "UPDATE vehicles SET status = 'Rented' WHERE id = ?",
            (chosen_vehicle_id,)
        )
        connection.commit()

        print(f"\nAwesome! You've rented the vehicle for {rental_days} days.")
        print(f"Your total cost will be ${total_bill:.2f}.")
    except sqlite3.Error as error_message:
        print(f"\nDatabase error: {error_message}")
    finally:
        connection.close()


def show_my_rental_history(current_user_id):
    """Shows a customer all the vehicles they have rented."""
    connection = connect_to_database()
    try:
        cursor = connection.cursor()
        # We use a JOIN here to grab the brand and model from the vehicles table
        # while looking at the rentals table.
        cursor.execute("""
            SELECT rentals.id, vehicles.brand, vehicles.model, rentals.days, rentals.total_cost, rentals.rental_status 
            FROM rentals
            JOIN vehicles ON rentals.vehicle_id = vehicles.id
            WHERE rentals.user_id = ?
        """, (current_user_id,))

        my_history = cursor.fetchall()

        print("\n--- MY RENTAL HISTORY ---")
        if not my_history:
            print("You haven't rented any vehicles yet.")
            return

        for record in my_history:
            rental_id = record[0]
            brand = record[1]
            model = record[2]
            days = record[3]
            cost = record[4]
            status = record[5]

            print(f"Receipt #{rental_id} | {brand} {model} | {days} days | Total: ${cost:.2f} | Status: {status}")
    except sqlite3.Error as error_message:
        print(f"\nDatabase error: {error_message}")
    finally:
        connection.close()


# ==========================================
# 6. MENUS (How the user interacts with the app)
# ==========================================
def show_admin_menu(logged_in_user):
    """The control panel for Admins."""
    while True:
        print(f"\n=== ADMIN DASHBOARD (Hello, {logged_in_user['username']}) ===")
        print("1. Add a New Vehicle")
        print("2. View All Vehicles")
        print("3. Change a Vehicle's Price")
        print("4. Remove a Vehicle")
        print("5. Log Out")

        choice = ask_for_text("What would you like to do? (1-5): ")

        if choice == '1':
            admin_add_new_vehicle()
        elif choice == '2':
            show_all_vehicles()
        elif choice == '3':
            admin_change_vehicle_price()
        elif choice == '4':
            admin_remove_vehicle()
        elif choice == '5':
            print("Logging out...")
            break
        else:
            print("\nInvalid choice. Please pick a number from 1 to 5.")


def show_customer_menu(logged_in_user):
    """The main screen for Customers."""
    while True:
        print(f"\n=== CUSTOMER MENU (Hello, {logged_in_user['username']}) ===")
        print("1. Browse Available Vehicles")
        print("2. Rent a Vehicle")
        print("3. View My Rental History")
        print("4. Log Out")

        choice = ask_for_text("What would you like to do? (1-4): ")

        if choice == '1':
            show_all_vehicles()
        elif choice == '2':
            rent_a_car(logged_in_user['id'])
        elif choice == '3':
            show_my_rental_history(logged_in_user['id'])
        elif choice == '4':
            print("Logging out...")
            break
        else:
            print("\nInvalid choice. Please pick a number from 1 to 4.")


def run_application():
    """This is the starting point of our program."""
    # First, make sure the database and tables exist!
    setup_database_tables()

    while True:
        print("\n" + "=" * 30)
        print("  WELCOME TO RENT-A-RIDE")
        print("=" * 30)
        print("1. Log In to your account")
        print("2. Register a new account")
        print("3. Quit")

        choice = ask_for_text("Please choose an option (1-3): ")

        if choice == '1':
            active_user = log_in_user()
            if active_user:
                # Direct the user to the correct menu based on their role
                if active_user['role'] == 'Admin':
                    show_admin_menu(active_user)
                else:
                    show_customer_menu(active_user)
        elif choice == '2':
            register_new_user()
        elif choice == '3':
            print("\nThanks for visiting! Have a great day.")
            sys.exit(0)  # Closes the program cleanly
        else:
            print("\nInvalid choice. Please pick 1, 2, or 3.")


# This tells Python to run the app when we execute the file.
if __name__ == "__main__":
    run_application()
