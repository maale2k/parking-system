from datetime import datetime

def vehicle_owner_menu():
    while True:
        print("\n===== Vehicle Owner Menu =====")
        print("1. Register Vehicle")
        print("2. View Permit Status")
        print("3. Request Permit")
        print("4. View Parking History")
        print("0. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            register_vehicle()
        elif choice == "2":
            view_permit_status()
        elif choice == "3":
            request_permit()
        elif choice == "4":
            view_parking_history()
        elif choice == "0":
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid choice. Please try again.")

def register_vehicle():
    plate = input("Enter plate number: ").upper().strip()
    model = input("Enter vehicle model: ").strip()
    color = input("Enter vehicle color: ").strip()

    if plate == "" or model == "" or color == "":
        print("All fields are required.")
        return

    try:
        with open("vehicles.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                if data[0] == plate:
                    print("Vehicle already registered.")
                    return
    except FileNotFoundError:
        pass

    ##Save vehicle
    with open("vehicles.txt", "a") as file:
        file.write(f"{plate},{model},{color}\n")

    print("Vehicle registered successfully.")

def view_permit_status():
    plate = input("Enter plate number: ").upper().strip()
    found = False

    try:
        with open("permits.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")

                if data[2] == plate:
                    print("\n--- Permit Information ---")
                    print(f"Permit Type  : {data[3]}")
                    print(f"Expiry Date : {data[4]}")
                    print(f"Status      : {data[5]}")
                    found = True
                    break
    except FileNotFoundError:
        print("Permit file not found.")

    if not found:
        print("No permit found for this vehicle.")

def request_permit():
    plate = input("Enter plate number: ").upper().strip()
    permit_type = input("Enter permit type (Daily / Monthly / Annual): ").strip()

    if plate == "" or permit_type == "":
        print("Invalid input.")
        return

    request_date = datetime.now().strftime("%Y-%m-%d")

    with open("requests.txt", "a") as file:
        file.write(f"{plate},{request_date},{permit_type}\n")

    print("Permit request submitted successfully.")

def view_parking_history():
    plate = input("Enter plate number: ").upper().strip()
    found = False

    try:
        with open("parking_logs.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")

                if data[0] == plate:
                    print("\n--- Parking Record ---")
                    print(f"Entry Time : {data[1]}")
                    print(f"Exit Time  : {data[2]}")
                    print(f"Space ID   : {data[3]}")
                    found = True
    except FileNotFoundError:
        print("Parking log file not found.")

    if not found:
        print("No parking history found for this vehicle.")

if __name__ == "__main__":
    vehicle_owner_menu()
