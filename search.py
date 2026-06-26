from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Button, Input
from textual.containers import Vertical, Horizontal
from rich.panel import Panel
from rich.align import Align

from utils import baca_data


class SearchDokumenScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static(Align.center(Panel("Masukkan nama dokumen untuk mencari", title="Search Dokumen", expand=False))),
            Input(placeholder="Nama dokumen...", id="keyword"),
            Horizontal(
                Button("Kembali", id="back"),
                Button("Cari", id="cari", variant="primary"),
                id="buttons"
            ),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()

        elif event.button.id == "cari":
            input_widget = self.query_one("#keyword", Input)
            keyword = input_widget.value.lower().strip()

            if not keyword:
                return

            data = baca_data()

            if not data:
                result = "Tidak ada data dokumen."
            else:
                hasil = []
                for d in data:
                    if keyword in d["nama"].lower():
                        hasil.append(d)

                if not hasil:
                    result = "Tidak ditemukan dokumen yang cocok."
                else:
                    lines = [f"Ditemukan {len(hasil)} dokumen", ""]
                    for i, d in enumerate(hasil, 1):
                        lines.append(f"{i}. {d['nama']}")
                        lines.append(f"   File    : {d['file']}")
                        lines.append(f"   Tanggal : {d['tanggal']}")
                        lines.append("")
                    result = "\n".join(lines)

            self.app.push_screen(HasilSearchScreen(result))


class HasilSearchScreen(Screen):
    def __init__(self, content: str):
        super().__init__()
        self.content = content

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static(Align.center(Panel(self.content, title="Hasil Pencarian", expand=False))),
            Input(placeholder="Cari lagi...", id="keyword"),
            Horizontal(
                Button("Kembali", id="back"),
                Button("Cari", id="cari", variant="primary"),
                id="buttons"
            ),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()

        elif event.button.id == "cari":
            input_widget = self.query_one("#keyword", Input)
            keyword = input_widget.value.lower().strip()

            if not keyword:
                return

            data = baca_data()

            if not data:
                result = "Tidak ada data dokumen."
            else:
                hasil = []
                for d in data:
                    if keyword in d["nama"].lower():
                        hasil.append(d)

                if not hasil:
                    result = "Tidak ditemukan dokumen yang cocok."
                else:
                    lines = [f"Ditemukan {len(hasil)} dokumen", ""]
                    for i, d in enumerate(hasil, 1):
                        lines.append(f"{i}. {d['nama']}")
                        lines.append(f"   File    : {d['file']}")
                        lines.append(f"   Tanggal : {d['tanggal']}")
                        lines.append("")
                    result = "\n".join(lines)

            self.app.push_screen(HasilSearchScreen(result))


def search_dokumen(app):
    app.push_screen(SearchDokumenScreen())
