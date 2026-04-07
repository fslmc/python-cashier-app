from fpdf import FPDF
from datetime import datetime
from pathlib import Path
import os
import subprocess
import platform

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
        "total": price * qty,
        "transaction_timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    }, None

def open_file(filepath):
    try:
        if platform.system() == 'Darwin':       # macOS
            subprocess.call(('open', filepath))
        elif platform.system() == 'Windows':    # Windows
            os.startfile(filepath)
        else:                                   # Linux
            subprocess.call(('xdg-open', filepath))
        return None
    except Exception as e:
        return e
        

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

def create_new_receipt(items):
    folder = Path("history")
    filename = f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = folder / filename  # Menggabungkan folder dan nama file
    
    # 2. Buat folder jika belum ada (exist_ok=True agar tidak error jika sudah ada)
    folder.mkdir(parents=True, exist_ok=True)

    pdf = FPDF()
    pdf.add_page()

    # PAGE TITLE
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 10, "STRUK PEMBELANJAAN", ln=True, align="C")
    pdf.ln(5)

    # TABLE HEADER
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(80, 10, "Item", border=1, align="C")
    pdf.cell(30, 10, "Harga", border=1, align="C")
    pdf.cell(30, 10, "Qty", border=1, align="C")
    pdf.cell(40, 10, "Total", border=1, align="C", ln=True)

    # TABLE CONTENT
    pdf.set_font("helvetica", "", 12)
    grand_total = 0
    for i in items:
        pdf.cell(80, 10, i['item_name'], border=1)
        pdf.cell(30, 10, f"{i['item_price']:,}", border=1)
        pdf.cell(30, 10, str(i['item_quantity']), border=1)
        pdf.cell(40, 10, f"{i['total']:,}", border=1, ln=True)
        grand_total += i['total']
        timestamp = i['transaction_timestamp']

    # TOTAL AKHIR & TIMESTAMP
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(140, 10, "GRAND TOTAL", border=1, align="R")
    pdf.cell(40, 10, f"{grand_total:,}", border=1, ln=True)
    pdf.cell(180, 5, f"{timestamp}", border=1, align="R", ln=True)

    pdf.output(str(filepath))
    return filepath



if __name__ == "__main__":
    woy = collect_all_items()

    print(woy)