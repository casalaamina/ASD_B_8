from utils import baca_data
import os


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def header():
    print("=" * 45)
    print("📊  SORTING DOKUMEN")
    print("=" * 45)

def quick_sort(data, key):
    if len(data) <= 1:
        return data

    pivot = data[len(data) // 2]

    kiri = []
    tengah = []
    kanan = []

    for item in data:
        if item[key].lower() < pivot[key].lower():
            kiri.append(item)

        elif item[key].lower() > pivot[key].lower():
            kanan.append(item)

        else:
            tengah.append(item)

    return quick_sort(kiri, key) + tengah + quick_sort(kanan, key)

def quick_sort_tanggal(data):
    if len(data) <= 1:
        return data

    pivot = data[len(data) // 2]

    kiri = []
    tengah = []
    kanan = []

    for item in data:
        if item['tanggal'] < pivot['tanggal']:
            kiri.append(item)

        elif item['tanggal'] > pivot['tanggal']:
            kanan.append(item)

        else:
            tengah.append(item)

    return (
        quick_sort_tanggal(kiri)
        + tengah
        + quick_sort_tanggal(kanan)
    )


def sort_dokumen():
    clear()
    header()

    data = baca_data()

    if not data:
        print("\n⚠️  Tidak ada data dokumen.")
        input("\nTekan ENTER untuk kembali...")
        return

    print("\n📌 Pilih metode sorting:")
    print("-" * 45)
    print("1. 🔤 Nama (A-Z)")
    print("2. 📅 Tanggal (Terlama → Terbaru)")
    print("-" * 45)

    pilihan = input("👉 Pilih (1/2): ")

    if pilihan == "1":
        hasil = quick_sort(data, 'nama')
        metode = "Nama (A-Z)"

    elif pilihan == "2":
        hasil = quick_sort_tanggal(data)
        metode = "Tanggal (Terlama → Terbaru)"

    else:
        print("\n❌ Pilihan tidak valid!")
        input("Tekan ENTER untuk kembali...")
        return

    print(f"\n📊 Hasil Sorting: {metode}")
    print("-" * 45)

    for i, d in enumerate(hasil, 1):
        print(f"{i}. 📌 {d['nama']}")
        print(f"    📁 File    : {d['file']}")
        print(f"    📅 Tanggal : {d['tanggal']}")
        print("-" * 45)

    input("\nTekan ENTER untuk kembali...")
