from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Button
from textual.containers import Vertical, Horizontal
from rich.panel import Panel
from rich.align import Align

from utils import baca_data



def merge_sort(data, key):
    if len(data) <= 1:
        return data

    mid = len(data) // 2
    left = merge_sort(data[:mid], key)
    right = merge_sort(data[mid:], key)

    return merge(left, right, key)


def merge(left, right, key):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i][key].lower() <= right[j][key].lower():
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

def merge_sort_tanggal(data):
    if len(data) <= 1:
        return data

    mid = len(data) // 2
    left = merge_sort_tanggal(data[:mid])
    right = merge_sort_tanggal(data[mid:])

    return merge_tanggal(left, right)


def merge_tanggal(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i]["tanggal"] <= right[j]["tanggal"]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

class SortDokumenScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static(Align.center(
                Panel("Pilih metode sorting", title="Sorting Dokumen", expand=False)
            )),
            Horizontal(
                Button("Nama (A-Z)", id="nama", variant="primary"),
                Button("Tanggal", id="tanggal", variant="primary"),
            ),
            Horizontal(
                Button("Kembali", id="back"),
            )
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()

        elif event.button.id == "nama":
            data = baca_data()
            if not data:
                result = "Tidak ada data dokumen."
            else:
                hasil = merge_sort(data, "nama")
                result = self.format_hasil(hasil, "Nama (A-Z)")
            self.app.push_screen(HasilSortScreen(result))

        elif event.button.id == "tanggal":
            data = baca_data()
            if not data:
                result = "Tidak ada data dokumen."
            else:
                hasil = merge_sort_tanggal(data)
                result = self.format_hasil(hasil, "Tanggal (Terlama → Terbaru)")
            self.app.push_screen(HasilSortScreen(result))

    def format_hasil(self, data, metode):
        lines = [f"Hasil Sorting: {metode}", ""]
        for i, d in enumerate(data, 1):
            lines.append(f"{i}. {d['nama']}")
            lines.append(f"   File    : {d['file']}")
            lines.append(f"   Tanggal : {d['tanggal']}")
            lines.append("")
        return "\n".join(lines)


class HasilSortScreen(Screen):
    def __init__(self, content: str):
        super().__init__()
        self.content = content

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static(Align.center(
                Panel(self.content, title="Hasil Sorting", expand=False)
            )),
            Horizontal(
                Button("Kembali", id="back"),
            )
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()


def sort_dokumen(app):
    app.push_screen(SortDokumenScreen())
