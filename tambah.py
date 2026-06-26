import datetime
import os
import shutil
from tkinter import Tk, filedialog

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Button, Input
from textual.containers import Vertical, Horizontal
from rich.panel import Panel
from rich.align import Align

from utils import baca_data, simpan_data


def pilih_file():
    root = Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Pilih Dokumen",
        filetypes=[
            ("PDF files", "*.pdf"),
            ("Word files", "*.docx")
        ]
    )

    return file_path


class TambahDokumenScreen(Screen):
    def __init__(self):
        super().__init__()
        self.file_path = ""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static(Align.center(Panel("Tambah Dokumen Baru", expand=False))),
            Input(placeholder="Nama dokumen...", id="nama"),
            Button("Pilih File", id="pilih", variant="primary"),
            Static("", id="file_info"),
            Horizontal(
                Button("Kembali", id="back"),
                 Button("Simpan", id="simpan", variant="success"),
                id="action_buttons"
            ),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()

        elif event.button.id == "pilih":
            file_path = pilih_file()
            info = self.query_one("#file_info", Static)

            if not file_path:
                info.update("Tidak ada file dipilih.")
                return

            if not (file_path.endswith(".pdf") or file_path.endswith(".docx")):
                info.update("Format harus PDF/DOCX.")
                return

            self.file_path = file_path
            info.update(f"File dipilih: {os.path.basename(file_path)}")

        elif event.button.id == "simpan":
            nama_input = self.query_one("#nama", Input)
            nama = nama_input.value.strip()
            info = self.query_one("#file_info", Static)

            if not nama:
                info.update("Nama dokumen tidak boleh kosong.")
                return

            if not self.file_path:
                info.update("Pilih file terlebih dahulu.")
                return

            data = baca_data()

            for item in data:
                if item["nama"].lower() == nama.lower():
                    info.update("Nama dokumen sudah ada.")
                    return

            nama_file = os.path.basename(self.file_path)

            folder_tujuan = "file_dokumen"
            if not os.path.exists(folder_tujuan):
                os.makedirs(folder_tujuan)

            tujuan = os.path.join(folder_tujuan, nama_file)

            shutil.copy(self.file_path, tujuan)

            tanggal = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            data.append({
                "nama": nama,
                "file": nama_file,
                "tanggal": tanggal
            })

            simpan_data(data)

            self.app.pop_screen()


def tambah_dokumen(app):
    app.push_screen(TambahDokumenScreen())
