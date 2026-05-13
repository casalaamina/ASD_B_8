from utils import baca_data
import os


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def header():
    print("=" * 45)
    print("🔍  SEARCH DOKUMEN")
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

def binary_search(data, keyword, key):
    low = 0
    high = len(data) - 1
    hasil = []

    while low <= high:
        mid = (low + high) // 2

        nilai = data[mid][key].lower()

        if keyword == nilai:
            # Ambil data tengah
            hasil.append(data[mid])

            # Cek ke kiri
            kiri = mid - 1
            while kiri >= 0 and data[kiri][key].lower() == keyword:
                hasil.append(data[kiri])
                kiri -= 1

            # Cek ke kanan
            kanan = mid + 1
            while kanan < len(data) and data[kanan][key].lower() == keyword:
                hasil.append(data[kanan])
                kanan += 1

            return hasil

        elif keyword < nilai:
            high = mid - 1

        else:
            low = mid + 1

    return hasil


def search_dokumen():
    clear()
    header()

    data = baca_data()

    if not data:
        print("\n⚠️  Tidak ada data dokumen.")
        input("\nTekan ENTER untuk kembali...")
        return

    keyword = input("\n🔎 Masukkan nama dokumen: ").lower()

    data_sorted = quick_sort(data, 'nama')

    hasil = binary_search(data_sorted, keyword, 'nama')

    print("\n📊 HASIL PENCARIAN")
    print("-" * 45)

    if not hasil:
        print("❌ Tidak ditemukan dokumen yang cocok.")

    else:
        print(f"✅ Ditemukan {len(hasil)} dokumen\n")

        for i, d in enumerate(hasil, 1):
            print(f"{i}. 📌 {d['nama']}")
            print(f"    📁 File    : {d['file']}")
            print(f"    📅 Tanggal : {d['tanggal']}")
            print("-" * 45)

    input("\nTekan ENTER untuk kembali...")
