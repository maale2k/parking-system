from datetime import datetime, timedelta

PERMITS_FILE = "permits.txt"
VEHICLES_FILE = "vehicles.txt"
PERMIT_TYPES_FILE = "permit_types.txt"

DATE_FORMAT = "%Y-%m-%d"


def permit_officer_menu():
    while True:
        print("\n===== Permit Officer Menu =====")
        print("1. Issue Permit")
        print("2. Renew Permit")
        print("3. Cancel Permit")
        print("4. Update Permit Information")
        print("5. View Permit List")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            issue_permit()
        elif choice == "2":
            renew_permit()
        elif choice == "3":
            cancel_permit()
        elif choice == "4":
            update_permit_information()
        elif choice == "5":
            view_permit_list()
        elif choice == "0":
            print("Exiting Permit Officer Menu...")
            break
        else:
            print("Invalid choice. Please try again.")

def ensure_file_exists(filename):
    try:
        file = open(filename, "r")
        file.close()
    except FileNotFoundError:
        file = open(filename, "w")
        file.close()


def setup_files():
    ensure_file_exists(PERMITS_FILE)
    ensure_file_exists(VEHICLES_FILE)
    ensure_file_exists(PERMIT_TYPES_FILE)


    try:
        with open(PERMIT_TYPES_FILE, "r") as file:
            content = file.read().strip()

        if content == "":
            with open(PERMIT_TYPES_FILE, "w") as file:
                file.write("Daily,10.00,Available\n")
                file.write("Monthly,100.00,Available\n")
                file.write("Annual,1000.00,Available\n")
    except FileNotFoundError:
        with open(PERMIT_TYPES_FILE, "w") as file:
            file.write("Daily,10.00,Available\n")
            file.write("Monthly,100.00,Available\n")
            file.write("Annual,1000.00,Available\n")


def read_lines(filename):
    try:
        with open(filename, "r") as file:
            return [line.strip() for line in file if line.strip() != ""]
    except FileNotFoundError:
        return []


def write_lines(filename, lines):
    with open(filename, "w") as file:
        for line in lines:
            file.write(line + "\n")


def append_line(filename, line):
    with open(filename, "a") as file:
        file.write(line + "\n")


def valid_text(value):
    return value.strip() != "" and "," not in value


def parse_date(date_string):
    try:
        return datetime.strptime(date_string, DATE_FORMAT)
    except ValueError:
        return None


def vehicle_exists(plate):
    lines = read_lines(VEHICLES_FILE)
    for line in lines:
        data = line.split(",")
        if len(data) >= 3 and data[0].upper() == plate.upper():
            return True
    return False


def permit_exists(plate):
    lines = read_lines(PERMITS_FILE)
    for line in lines:
        data = line.split(",")
        if len(data) >= 6 and data[1].upper() == plate.upper() and data[5] != "Cancelled":
            return True
    return False


def get_permit_type_details(permit_type):
    lines = read_lines(PERMIT_TYPES_FILE)
    for line in lines:
        data = line.split(",")
        if len(data) >= 3 and data[0].lower() == permit_type.lower():
            return data
    return None


# =========================
# PERMIT OFFICER FUNCTIONS
# =========================
def issue_permit():
    print("\n=== Issue Permit ===")
    owner_name = input("Enter owner name: ").strip()
    plate = input("Enter vehicle plate number: ").strip().upper()
    permit_type = input("Enter permit type (Daily/Monthly/Annual): ").strip().capitalize()

    if not valid_text(owner_name):
        print("Invalid owner name.")
        return

    if not valid_text(plate):
        print("Invalid plate number.")
        return

    if not vehicle_exists(plate):
        print("Vehicle is not registered.")
        return

    permit_type_data = get_permit_type_details(permit_type)
    if permit_type_data is None:
        print("Permit type not found.")
        return

    if permit_type_data[2] != "Available":
        print("This permit type is currently unavailable.")
        return

    if permit_exists(plate):
        print("This vehicle already has a permit.")
        return

    if permit_type.lower() == "daily":
        expiry_date = datetime.now() + timedelta(days=1)
    elif permit_type.lower() == "monthly":
        expiry_date = datetime.now() + timedelta(days=30)
    elif permit_type.lower() == "annual":
        expiry_date = datetime.now() + timedelta(days=365)
    else:
        print("Invalid permit type.")
        return

    payment = permit_type_data[1]
    status = "Active"

    append_line(
        PERMITS_FILE,
        f"{owner_name},{plate},{permit_type},{expiry_date.strftime(DATE_FORMAT)},{payment},{status}"
    )

    print("Permit issued successfully.")


def renew_permit():
    print("\n=== Renew Permit ===")
    plate = input("Enter vehicle plate number: ").strip().upper()

    if not valid_text(plate):
        print("Invalid plate number.")
        return

    lines = read_lines(PERMITS_FILE)
    updated = []
    found = False

    for line in lines:
        data = line.split(",")
        if len(data) >= 6 and data[1].upper() == plate.upper() and data[5] != "Cancelled":
            found = True

            permit_type = data[2]
            current_expiry = parse_date(data[3])

            if current_expiry is None:
                print("Invalid expiry date in record.")
                return

            if permit_type.lower() == "daily":
                new_expiry = current_expiry + timedelta(days=1)
            elif permit_type.lower() == "monthly":
                new_expiry = current_expiry + timedelta(days=30)
            elif permit_type.lower() == "annual":
                new_expiry = current_expiry + timedelta(days=365)
            else:
                new_expiry = current_expiry + timedelta(days=30)

            data[3] = new_expiry.strftime(DATE_FORMAT)
            data[5] = "Active"
            updated.append(",".join(data))
        else:
            updated.append(line)

    if not found:
        print("Permit not found.")
        return

    write_lines(PERMITS_FILE, updated)
    print("Permit renewed successfully.")


def cancel_permit():
    print("\n=== Cancel Permit ===")
    plate = input("Enter vehicle plate number: ").strip().upper()

    if not valid_text(plate):
        print("Invalid plate number.")
        return

    lines = read_lines(PERMITS_FILE)
    updated = []
    found = False

    for line in lines:
        data = line.split(",")
        if len(data) >= 6 and data[1].upper() == plate.upper() and data[5] != "Cancelled":
            found = True
            data[5] = "Cancelled"
            updated.append(",".join(data))
        else:
            updated.append(line)

    if not found:
        print("Permit not found.")
        return

    write_lines(PERMITS_FILE, updated)
    print("Permit cancelled successfully.")


def update_permit_information():
    print("\n=== Update Permit Information ===")
    plate = input("Enter vehicle plate number to update: ").strip().upper()

    if not valid_text(plate):
        print("Invalid plate number.")
        return

    lines = read_lines(PERMITS_FILE)
    updated = []
    found = False

    for line in lines:
        data = line.split(",")
        if len(data) >= 6 and data[1].upper() == plate.upper() and data[5] != "Cancelled":
            found = True
            print("Current Record:", line)

            new_owner = input("Enter new owner name: ").strip()
            new_plate = input("Enter new plate number: ").strip().upper()
            new_permit_type = input("Enter new permit type (Daily/Monthly/Annual): ").strip().capitalize()

            if not valid_text(new_owner):
                print("Invalid owner name.")
                return

            if not valid_text(new_plate):
                print("Invalid plate number.")
                return

            permit_type_data = get_permit_type_details(new_permit_type)
            if permit_type_data is None:
                print("Permit type not found.")
                return

            data[0] = new_owner
            data[1] = new_plate
            data[2] = new_permit_type
            data[4] = permit_type_data[1]

            updated.append(",".join(data))
        else:
            updated.append(line)

    if not found:
        print("Permit not found.")
        return

    write_lines(PERMITS_FILE, updated)
    print("Permit information updated successfully.")


def view_permit_list():
    print("\n=== View Permit List ===")
    lines = read_lines(PERMITS_FILE)

    if len(lines) == 0:
        print("No permits found.")
        return

    today = datetime.now()

    for line in lines:
        data = line.split(",")
        if len(data) >= 6:
            expiry = parse_date(data[3])

            if expiry is not None and data[5] != "Cancelled":
                if expiry < today:
                    data[5] = "Expired"

            print(",".join(data))

if __name__ == "__main__":
    permit_officer_menu()