from fpdf import FPDF
from datetime import datetime
from pathlib import Path
import os
import subprocess
import platform

def create_single_item():
    print("\n--- Input Data Barang (Kosongkan Nama untuk SELESAI) ---")
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
        "total": price * qty
    }, None

def open_file(filepath):
    path = Path(filepath)
    
    if not path.exists():
        print(f"Error: The file {path} does not exist.")
        return

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
        

def collect_transaction():
    # 1. INPUT SEKALI DI AWAL
    print("=== Data Pelanggan ===")
    cust_name = input("Nama Customer: ")
    cust_phone = input("Nomor HP     : ")
    
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

    total_kotor = sum(i['total'] for i in item_list)
    diskon = 0
    if total_kotor > 50000:
        diskon = total_kotor * 0.1  # 10%

    total_akhir = total_kotor - diskon

    # 3. GABUNGKAN SEMUA DATA
    return {
        "customer_name": cust_name,
        "customer_phone": cust_phone,
        "items": item_list,
        "total_kotor": total_kotor,
        "diskon": diskon,
        "grand_total": total_akhir,
        "transaction_timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    }

    return transaction_data

def create_new_receipt(data):
    if not data or not data['items']:
        return None

    folder = Path("history")
    filename = f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = folder / filename  # Menggabungkan folder dan nama file
    
    # 2. Buat folder jika belum ada (exist_ok=True agar tidak error jika sudah ada)
    folder.mkdir(parents=True, exist_ok=True)

    pdf = FPDF()
    pdf.add_page()

    # PAGE TITLE
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 10, "Struk Pembelian - Alesha Mart", ln=True, align="C")
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 10, f"Waktu: {data['transaction_timestamp']}", ln=True, align="C")
    pdf.ln(5)

    # DATA PELANGGAN
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, "Data Customer:", ln=True)
    pdf.set_font('Helvetica', '', 12)
    pdf.cell(0, 8, f"Nama: {data['customer_name']}", ln=True)
    pdf.cell(0, 8, f"No HP: {data['customer_phone']}", ln=True)
    pdf.ln(5)

    # TABLE HEADER
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(80, 10, "Item", border=1)
    pdf.cell(30, 10, "Harga", border=1, align="C")
    pdf.cell(30, 10, "Qty", border=1, align="C")
    pdf.cell(40, 10, "Total", border=1, align="C", ln=True)

    # TABLE CONTENT
    pdf.set_font("Helvetica", "", 12)
    for i in data['items']:
        pdf.cell(80, 10, i['item_name'], border=1)
        pdf.cell(30, 10, f"{i['item_price']:,.0f}", border=1, align="R")
        pdf.cell(30, 10, str(i['item_quantity']), border=1, align="C")
        pdf.cell(40, 10, f"{i['total']:,.0f}", border=1, align="R", ln=True)

    # RINGKASAN PEMBAYARAN
    pdf.set_font("Helvetica", "B", 12)
    
    # Total Kotor
    pdf.cell(140, 10, "Total Harga", border=1, align="R")
    pdf.cell(40, 10, f"{data['total_kotor']:,.0f}", border=1, align="R", ln=True)
    
    # Row diskon hanya tampil jika mendapatkan diskon
    if data['diskon'] > 0:
        pdf.set_text_color(255, 0, 0)
        pdf.cell(140, 10, "Diskon (10%)", border=1, align="R")
        pdf.cell(40, 10, f"-{data['diskon']:,.0f}", border=1, align="R", ln=True)
        pdf.set_text_color(0, 0, 0)

    # Grand Total
    pdf.cell(140, 10, "GRAND TOTAL", border=1, align="R")
    pdf.cell(40, 10, f"{data['grand_total']:,.0f}", border=1, align="R", ln=True)

    pdf.output(str(filepath))
    return filepath



if __name__ == "__main__":
    woy = collect_transaction()

    print(woy)