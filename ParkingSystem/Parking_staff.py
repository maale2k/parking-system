from datetime import datetime

PARKING_SPACES_FILE = "parking_spaces.txt"
PARKING_LOGS_FILE = "parking_logs.txt"
TEMP_PASSES_FILE = "temp_passes.txt"

def parking_staff_menu():
    while True:
        print("\n===== Parking Staff Menu =====")
        print("1. Check Availability:")
        print("2. Record Vehicle Entry:")
        print("3. Record Vehicle Exit:")
        print("4. Issue Temporary Pass:")
        print("5. View Daily Logs:")
        print("0. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            check_availability()
        elif choice == "2":
            record_vehicle_entry()
        elif choice == "3":
            record_vehicle_exit()
        elif choice == "4":
            issue_temporary_pass()
        elif choice == "5":
            view_daily_logs()
        elif choice == "0":
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid choice. Please try again.")

def ensure_parking_spaces_file():
    try:
        with open(PARKING_SPACES_FILE, "r") as file:
            pass
    except FileNotFoundError:
        with open(PARKING_SPACES_FILE, "w") as file:
            file.write("L1-01,Regular,Available\n")
            file.write("L1-02,Regular,Occupied\n")
            file.write("L1-03,Regular,Available\n")
            file.write("L2-01,Reserved,Available\n")
            file.write("L2-02,Reserved,Available\n")
            file.write("E1-01,Electric,Available\n")
            file.write("E1-02,Electric,Occupied\n")


def load_spaces():
    ensure_parking_spaces_file()
    spaces = []

    try:
        with open(PARKING_SPACES_FILE, "r") as file:
            for line in file:
                data = line.strip().split(",")
                if len(data) == 3:
                    spaces.append(data)
    except FileNotFoundError:
        print("Parking spaces file not found.")

    return spaces


def save_spaces(spaces):
    with open(PARKING_SPACES_FILE, "w") as file:
        for space in spaces:
            file.write(",".join(space) + "\n")


def find_available_space(space_type):
    spaces = load_spaces()
    for space in spaces:
        if space[1].lower() == space_type.lower() and space[2].lower() == "available":
            return space[0]
    return None


def mark_space_status(space_id, new_status):
    spaces = load_spaces()
    updated = False

    for space in spaces:
        if space[0] == space_id:
            space[2] = new_status
            updated = True
            break

    if updated:
        save_spaces(spaces)

    return updated


def is_vehicle_currently_parked(plate):
    try:
        with open(PARKING_LOGS_FILE, "r") as file:
            for line in file:
                data = line.strip().split(",")
                # Expected:
                # plate,entry_time,exit_time,space_id,status
                if len(data) == 5 and data[0] == plate and data[4] == "IN":
                    return True
    except FileNotFoundError:
        pass

    return False

def check_availability():
    spaces = load_spaces()

    regular_count = 0
    reserved_count = 0
    electric_count = 0

    print("\n--- Available Parking Spaces ---")
    print("Regular:")
    for space in spaces:
        if space[1] == "Regular" and space[2] == "Available":
            print(space[0])
            regular_count += 1

    print("\nReserved:")
    for space in spaces:
        if space[1] == "Reserved" and space[2] == "Available":
            print(space[0])
            reserved_count += 1

    print("\nElectric:")
    for space in spaces:
        if space[1] == "Electric" and space[2] == "Available":
            print(space[0])
            electric_count += 1

    print("\nSummary:")
    print("Regular available :", regular_count)
    print("Reserved available:", reserved_count)
    print("Electric available:", electric_count)

def record_vehicle_entry():
    plate = input("Enter plate number: ").upper().strip()
    space_type = input("Enter required space type (Regular / Reserved / Electric): ").strip()

    if plate == "" or space_type == "":
        print("Plate number and space type are required.")
        return

    if space_type.lower() not in ["regular", "reserved", "electric"]:
        print("Invalid space type.")
        return

    if is_vehicle_currently_parked(plate):
        print("This vehicle is already inside the parking lot.")
        return

    available_space = find_available_space(space_type)

    if available_space is None:
        print("No available parking space for this type.")
        return

    entry_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(PARKING_LOGS_FILE, "a") as file:
        file.write(f"{plate},{entry_time},-,{available_space},IN\n")

    mark_space_status(available_space, "Occupied")
    print("Vehicle entry recorded successfully.")
    print("Assigned space:", available_space)
    print("Entry time:", entry_time)

def record_vehicle_exit():
    plate = input("Enter plate number: ").upper().strip()

    if plate == "":
        print("Plate number is required.")
        return

    logs = []
    found = False
    freed_space = ""

    try:
        with open(PARKING_LOGS_FILE, "r") as file:
            for line in file:
                data = line.strip().split(",")
                if len(data) == 5 and data[0] == plate and data[4] == "IN" and not found:
                    exit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    data[2] = exit_time
                    data[4] = "OUT"
                    freed_space = data[3]
                    found = True
                logs.append(data)
    except FileNotFoundError:
        print("Parking logs file not found.")
        return

    if not found:
        print("No active parking record found for this vehicle.")
        return

    with open(PARKING_LOGS_FILE, "w") as file:
        for log in logs:
            file.write(",".join(log) + "\n")

    mark_space_status(freed_space, "Available")
    print("Vehicle exit recorded successfully.")
    print("Freed space:", freed_space)
    print("Exit time:", exit_time)

def issue_temporary_pass():
    plate = input("Enter visitor plate number: ").upper().strip()
    fee = input("Enter fee: ").strip()
    validity = input("Enter validity (example: 1 Day / 3 Hours): ").strip()

    if plate == "" or fee == "" or validity == "":
        print("All fields are required.")
        return

    try:
        float(fee)
    except ValueError:
        print("Fee must be numeric.")
        return

    issue_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(TEMP_PASSES_FILE, "a") as file:
        file.write(f"{plate},{fee},{validity},{issue_date}\n")

    print("Temporary pass issued successfully.")

def view_daily_logs():
    today = datetime.now().strftime("%Y-%m-%d")
    found = False

    print("\n--- Daily Parking Logs ---")

    try:
        with open(PARKING_LOGS_FILE, "r") as file:
            for line in file:
                data = line.strip().split(",")
                if len(data) == 5 and data[1].startswith(today):
                    print("Plate      :", data[0])
                    print("Entry Time :", data[1])
                    print("Exit Time  :", data[2])
                    print("Space ID   :", data[3])
                    print("Status     :", data[4])
                    print("-" * 30)
                    found = True
    except FileNotFoundError:
        print("Parking logs file not found.")
        return

    if not found:
        print("No logs found for today.")

if __name__ == "__main__":
    parking_staff_menu()