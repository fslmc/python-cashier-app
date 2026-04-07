from fpdf import FPDF
from datetime import datetime

def create_single_item():
    print("--- Input Data (Kosongkan Nama Barang untuk SELESAI) ---")

    # Penanda berhenti
    name = input("Nama barang: ")
    if not name:
        return None, "EOF"
    
    try:
        price = float(input("Harga barang: "))
        qty = int(input("Jumlah barang: "))
    except ValueError:
        return None, "INVALID_INPUT"

    return {
        "item_name": name,
        "item_price": price,
        "item_quantity": qty,
        "transaction_timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    }, None


def collect_all_items():
    item_list = []

    while True:
        item, err = create_single_item()
        if err == "EOF":
            break
        if err == "INVALID_INPUT":
            print(">> Error: Harga atau jumlah harus angka. Ulangi barang ini.")
            continue

        item_list.append(item)
        print(f"Berhasil menambah: {item['item_name']}")

    return item_list






if __name__ == "__main__":
    woy = collect_all_items()

    print(woy)