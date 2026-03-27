def administrator_menu():

    while True:

        print("\n===== System Administrator Menu =====")
        print("1. Add Parking Space:")
        print("2. Remove Parking Space:")
        print("3. Update Parking Space:")
        print("4. Add Permit Type:")
        print("5. Update Permit Type:")
        print("6. Generate Reports:")
        print("7. View All Records:")
        print("8. Back to Main Menu:")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_parking_space()

        elif choice == "2":
            remove_parking_space()

        elif choice == "3":
            update_parking_space()

        elif choice == "4":
            add_permit_type()

        elif choice == "5":
            update_permit_type()

        elif choice == "6":
            generate_reports()

        elif choice == "7":
            view_all_records()

        elif choice == "8":
            break

        else:
            print("Invalid choice. Please try again.")

SPACES_FILE = "spaces.txt"
PERMITS_FILE = "permits.txt"

def add_parking_space():
    space_id = input("Enter Space ID: ")
    space_type = input("Enter Space Type (Regular/Reserved/Electric): ")
    availability = "Available"

    try:
        with open(SPACES_FILE, "a") as file:
            file.write(space_id + "," + space_type + "," + availability + "\n")

        print("Parking space added successfully.")

    except:
        print("Error writing to file.")


def remove_parking_space():
    space_id = input("Enter Space ID to remove: ")
    found = False

    try:
        with open(SPACES_FILE, "r") as file:
            lines = file.readlines()

        with open(SPACES_FILE, "w") as file:
            for line in lines:
                data = line.strip().split(",")

                if data[0] != space_id:
                    file.write(line)
                else:
                    found = True

        if found:
            print("Parking space removed.")
        else:
            print("Space ID not found.")

    except:
        print("Error accessing file.")


def update_parking_space():
    space_id = input("Enter Space ID to update: ")
    found = False

    try:
        with open(SPACES_FILE, "r") as file:
            lines = file.readlines()

        with open(SPACES_FILE, "w") as file:
            for line in lines:
                data = line.strip().split(",")

                if data[0] == space_id:
                    new_type = input("Enter new space type: ")
                    new_availability = input("Enter availability (Available/Occupied): ")
                    file.write(space_id + "," + new_type + "," + new_availability + "\n")
                    found = True
                else:
                    file.write(line)

        if found:
            print("Parking space updated successfully.")
        else:
            print("Space ID not found.")

    except:
        print("Error updating file.")


def add_permit_type():
    permit_type = input("Enter Permit Type (Daily/Monthly/Annual): ")
    price = input("Enter Permit Price: ")

    try:
        with open(PERMITS_FILE, "a") as file:
            file.write(permit_type + "," + price + "\n")

        print("Permit type added successfully.")

    except:
        print("Error writing to file.")


def update_permit_type():
    permit_type = input("Enter Permit Type to update: ")
    found = False

    try:
        with open(PERMITS_FILE, "r") as file:
            lines = file.readlines()

        with open(PERMITS_FILE, "w") as file:
            for line in lines:
                data = line.strip().split(",")

                if data[0] == permit_type:
                    new_price = input("Enter new permit price: ")
                    file.write(permit_type + "," + new_price + "\n")
                    found = True
                else:
                    file.write(line)

        if found:
            print("Permit updated successfully.")
        else:
            print("Permit type not found.")

    except:
        print("Error updating permit file.")


def view_all_records():

    print("\n--- Parking Spaces ---")

    try:
        with open(SPACES_FILE, "r") as file:
            for line in file:
                print(line.strip())
    except:
        print("No parking space data found.")

    print("\n--- Permit Types ---")

    try:
        with open(PERMITS_FILE, "r") as file:
            for line in file:
                print(line.strip())
    except:
        print("No permit data found.")


def generate_reports():
    total_spaces = 0
    available_spaces = 0
    occupied_spaces = 0

    try:
        with open(SPACES_FILE, "r") as file:
            for line in file:
                data = line.strip().split(",")
                total_spaces += 1

                if data[2] == "Available":
                    available_spaces += 1
                else:
                    occupied_spaces += 1

        print("\n--- Parking Report ---")
        print("Total Spaces:", total_spaces)
        print("Available Spaces:", available_spaces)
        print("Occupied Spaces:", occupied_spaces)

    except:
        print("Error reading parking data.")

if __name__ == "__main__":
    administrator_menu()
