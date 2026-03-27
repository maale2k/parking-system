from system_admin import administrator_menu
from Parking_staff import parking_staff_menu
from permit_officer_function import permit_officer_menu
from vehicle_owner import vehicle_owner_menu

def main_menu():
    while True:
        print("\n===== Parking Lot System =====")
        print("1. System Administrator:")
        print("2. Parking Staff:")
        print("3. Permit Officer:")
        print("4. Vehicle Owner:")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            administrator_menu()
        elif choice == "2":
            parking_staff_menu()
        elif choice == "3":
            permit_officer_menu()
        elif choice == "4":
            vehicle_owner_menu()
        elif choice == "0":
            print("Exiting system...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_menu()
