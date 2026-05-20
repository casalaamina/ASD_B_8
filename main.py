# python -m pip install rich
# python -m pip install textual
# itu kalo blm install 

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static
from textual.containers import Vertical, Horizontal
from textual.screen import Screen
from rich.panel import Panel
from rich.align import Align

from tambah import tambah_dokumen
from lihat import lihat_dokumen
from proses import proses_dokumen
from search import search_dokumen
from sort import sort_dokumen
from utils import baca_riwayat


class MenuScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static(Align.center(Panel("SISTEM DOKUMEN", expand=False))),
            Horizontal(
                Button("Lihat Dokumen", id="lihat"),
                Button("Tambah Dokumen", id="tambah"),
                Button("Proses (LIFO)", id="proses"),
            ),
            Horizontal(
                Button("Searching", id="search"),
                Button("Sorting", id="sort"),
                Button("Riwayat", id="riwayat"),
            ),
            Horizontal(
                Button("Keluar", id="keluar", variant="error"),
            ),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "lihat":
            lihat_dokumen(self.app)

        elif event.button.id == "tambah":
            tambah_dokumen(self.app)

        elif event.button.id == "proses":
            proses_dokumen(self.app)

        elif event.button.id == "search":
            search_dokumen(self.app)

        elif event.button.id == "sort":
            sort_dokumen(self.app)

        elif event.button.id == "riwayat":
            self.app.push_screen(RiwayatScreen())

        elif event.button.id == "keluar":
            self.app.exit()

class RiwayatScreen(Screen):
    def compose(self) -> ComposeResult:
        raw = baca_riwayat()

        yield Header()

        if not raw:
            yield Vertical(
                Static(Panel("Belum ada riwayat.", expand=False)),
                Button("Kembali", id="back"),
            )
            yield Footer()
            return

        items = []

        for i, item in enumerate(raw, 1):
            if isinstance(item, dict):
                nama = item.get("nama", "-")
                tanggal = item.get("tanggal", "-")
                file = item.get("file", "-")

                content = (
                    f"Nama    : {nama}\n"
                    f"Tanggal : {tanggal}\n"
                    f"File    : {file}"
                )
            else:
                content = str(item)

            items.append(
                Static(Panel(content, title=f"Dokumen {i}", expand=False))
            )

        yield Vertical(
            *items,
            Horizontal(
                Button("Kembali", id="back"),
            )
            
        )

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()
  
                  
class DokumenApp(App):
    CSS = """
    Screen {
        align: center middle;
    }

    Vertical {
        width: 60%;
        height: auto;
        align: center middle;
        padding: 2;
        border: round white;
    }

    Horizontal {
        height: auto;
        align: center middle;
        padding: 1;
    }

    Button {
        margin: 1;
        width: 20;
    }
    """

    def on_mount(self) -> None:
        self.push_screen(MenuScreen())


if __name__ == "__main__":
    DokumenApp().run()
