from pdf_factory import create_new_receipt, collect_all_items, open_file 
from history import collect_all_receipt, open_receipt

def show_menu():
    print("\n" + "-" * 40)
    print("          MAIN MENU")
    print("-" * 40)
    print("1. 📝 Create New Receipt")
    print("2. 📜 View Receipt History")
    print("3. 🚪 Exit")
    print("-" * 40)

def handle_create_receipt():
    print("\n✅ Creating new receipt...")
    items = collect_all_items()
    if items:
        filepath = create_new_receipt(items) 
        input(f"\n✅ Receipt created at {filepath}! Press Enter to open the receipt...")
        open_file(filepath)
    else:
        input("\n⚠️ No items added. Press Enter...")


def handle_view_history():
    print("\n" + "-" * 20)
    print("📜 RECEIPT HISTORY")
    print("-" * 20)
    
    receipts, err = collect_all_receipt()

    if err:
        print(f"❌ Critical Error: {err}")
        return

    if not receipts:
        print("\n📭 No receipts found in history.")
        input("↩ Press ENTER to go back....")
        return
    

        # displaying file list with order numbers for readability
    for i, file in enumerate(receipts, 1):
        print(f"{i}. {file.name}")
        
    print("00. Back to Main Menu")

    while True:
        choice = input("\nEnter file number to open (or 00 to go back): ").strip()

        # break condition to go back to main menu
        if choice == "00":
            break

        # file selection
        try:
            index = int(choice) - 1
            if 0 <= index < len(receipts):
                selected_file = receipts[index]
                print(f"Opening: {selected_file.name}...")
                success, err = open_receipt(selected_file)
                if not success:
                    print(f"❌ Failed to open file: {err}")
                else:
                    print("✅ Opened successfully!")
            else:
                print("❌ Invalid number. Please pick a number from the list.")
        except ValueError:
            print("❌ Please enter a valid number.")



def main():

    actions = {
        1: handle_create_receipt,
        2: handle_view_history,
    }


    print("\n" + "=" * 40)
    print("   🛒  WELCOME TO CASHIER APP  🛒")
    print("=" * 40 + "\n")

    while True:
        show_menu()

        try:
            choice = input("\nEnter your choice (1-3): ").strip()

            if not choice:
                print("\nInput cannot be empty!")
                input("\nPress enter to continue...")
                continue

            choice_num = int(choice)
            if choice_num == 3:
                print("\n👋 Thank you for using Cashier App. Goodbye!\n")
                break

            action = actions.get(choice_num)
            if action:
                action()
            else:
                print("\n❌ Invalid choice! Please enter 1, 2, or 3.")
                input("Press Enter to try again...")

        except ValueError:
            print("\n❌ Please enter a valid number (1, 2, or 3)!")
            input("Press Enter to try again...")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!\n")
            break



if __name__ == "__main__":
    main()