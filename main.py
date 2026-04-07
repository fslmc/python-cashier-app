from pdf_factory import create_new_receipt, collect_all_items, open_file 

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
        input(f"\n✅ Receipt created at {filepath}! Press Enter...")
        open_file(filepath)
    else:
        input("\n⚠️ No items added. Press Enter...")

def main():

    actions = {
        1: handle_create_receipt,
        # 2: handle_view_history,
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