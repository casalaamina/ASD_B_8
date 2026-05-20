import os

DATA_FILE = "data.txt"
RIWAYAT_FILE = "riwayat.txt"


def baca_data():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as file:
        lines = file.readlines()

    data = []
    for line in lines:
        parts = line.strip().split("|")
        if len(parts) == 3:
            nama, file_doc, tanggal = parts
            data.append({
                "nama": nama.strip(),
                "file": file_doc.strip(),
                "tanggal": tanggal.strip()
            })
    return data


def simpan_data(data):
    with open(DATA_FILE, "w") as file:
        for d in data:
            file.write(f"{d['nama']}|{d['file']}|{d['tanggal']}\n")


def tambah_riwayat(dokumen):
    with open(RIWAYAT_FILE, "a") as file:
        file.write(f"{dokumen['nama']}|{dokumen['file']}|{dokumen['tanggal']}\n")


def baca_riwayat():
    if not os.path.exists(RIWAYAT_FILE):
        return []

    with open(RIWAYAT_FILE, "r") as file:
        lines = file.readlines()

    data = []
    for line in lines:
        parts = line.strip().split("|")
        if len(parts) == 3:
            nama, file_doc, tanggal = parts
            data.append({
                "nama": nama.strip(),
                "file": file_doc.strip(),
                "tanggal": tanggal.strip()
            })

    data.reverse()
    return data


def format_riwayat(riwayat):
    if not riwayat:
        return []

    max_nama = max(len(r["nama"]) for r in riwayat)
    max_file = max(len(r["file"]) for r in riwayat)
    max_tanggal = max(len(r["tanggal"]) for r in riwayat)

    hasil = []
    header = f"{'NAMA'.ljust(max_nama)} | {'FILE'.ljust(max_file)} | {'TANGGAL'.ljust(max_tanggal)}"
    garis = "-" * len(header)
    hasil.append(header)
    hasil.append(garis)

    for r in riwayat:
        baris = f"{r['nama'].ljust(max_nama)} | {r['file'].ljust(max_file)} | {r['tanggal'].ljust(max_tanggal)}"
        hasil.append(baris)

    return hasil
