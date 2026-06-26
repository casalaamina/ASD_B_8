from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Button
from textual.containers import Vertical, Horizontal
from rich.panel import Panel
from rich.align import Align

from utils import baca_data, simpan_data, tambah_riwayat


class ProsesDokumenScreen(Screen):
    def compose(self) -> ComposeResult:
        data = baca_data()

        if not data:
            content = "Tidak ada dokumen untuk diproses."
        else:
            dokumen = data[-1]
            content = "\n".join([
                "Dokumen teratas akan diproses:",
                "",
                f"Nama    : {dokumen['nama']}",
                f"File    : {dokumen['file']}",
                f"Tanggal : {dokumen['tanggal']}",
            ])

        yield Header()
        yield Vertical(
            Static(Align.center(Panel(content, title="Proses Dokumen (LIFO)", expand=False))),

            Horizontal(
                Button("Kembali", id="back"),
                Button("Proses Sekarang", id="proses", variant="primary"),
                
                id="button-row"
            ),

        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()

        elif event.button.id == "proses":
            data = baca_data()

            if not data:
                return

            dokumen = data.pop()
            simpan_data(data)
            tambah_riwayat(dokumen)

            result = "\n".join([
                "Dokumen berhasil diproses.",
                "",
                f"Nama    : {dokumen['nama']}",
                f"File    : {dokumen['file']}",
                f"Tanggal : {dokumen['tanggal']}",
                "",
                "Dokumen telah dipindahkan ke riwayat."
            ])

            self.app.pop_screen()
            self.app.push_screen(HasilProsesScreen(result))


class HasilProsesScreen(Screen):
    def __init__(self, content: str):
        super().__init__()
        self.content = content

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static(Align.center(Panel(self.content, title="Hasil Proses", expand=False))),
            Horizontal(
                Button("Kembali", id="back"),
                id="button-row"
            ),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()


def proses_dokumen(app):
    app.push_screen(ProsesDokumenScreen())
