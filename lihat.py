from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Button, Input
from textual.containers import Vertical, Horizontal
from rich.panel import Panel
from rich.align import Align
from datetime import datetime
import os
import shutil
from tkinter import Tk, filedialog

from utils import baca_data, simpan_data


def pilih_file():
    root = Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Pilih Dokumen",
        filetypes=[("PDF files", "*.pdf"), ("Word files", "*.docx")],
    )

    return file_path


class LihatDokumenScreen(Screen):
    def compose(self) -> ComposeResult:
        data = baca_data()

        if not data:
            content = "Tidak ada dokumen."
        else:
            lines = []
            for i, doc in enumerate(reversed(data), start=1):
                lines.append(f"{i}. {doc['nama']}")
                lines.append(f"   File    : {doc['file']}")
                lines.append(f"   Tanggal : {doc['tanggal']}")
                lines.append("")
            content = "\n".join(lines)

        yield Header()
        yield Vertical(
            Static(Align.center(Panel(content, title="Daftar Dokumen", expand=False))),
            Horizontal(
                Button("Kembali", id="back"),
                Button("Delete", id="delete", variant="error"),
                Button("Update", id="update", variant="primary"),
            ),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()
        elif event.button.id == "update":
            self.app.push_screen(UpdateScreen())
        elif event.button.id == "delete":
            self.app.push_screen(DeleteScreen())


class UpdateScreen(Screen):
    def __init__(self):
        super().__init__()
        self.file_path = ""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static("Masukkan nomor dokumen yang ingin diupdate"),
            Input(placeholder="Nomor dokumen", id="nomor"),
            Input(placeholder="Nama baru (opsional)", id="nama"),
            Button("Pilih File Baru", id="pilih", variant="primary"),
            Static("", id="file_info"),
            Horizontal(
                Button("Simpan", id="simpan", variant="success"),
                Button("Kembali", id="back"),
            ),
            Static("", id="error"),
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
            nomor_input = self.query_one("#nomor", Input)
            nama_input = self.query_one("#nama", Input)
            error_text = self.query_one("#error", Static)
            info = self.query_one("#file_info", Static)

            nomor = nomor_input.value.strip()
            nama = nama_input.value.strip()

            if not nomor:
                error_text.update("Nomor harus diisi")
                return

            if not nomor.isdigit():
                error_text.update("Nomor harus berupa angka")
                return

            data = baca_data()
            index = int(nomor)

            if index < 1 or index > len(data):
                error_text.update("Nomor tidak valid")
                return

            if not nama and not self.file_path:
                error_text.update("Isi nama atau pilih file baru")
                return

            real_index = len(data) - index

            if nama:
                data[real_index]["nama"] = nama

            if self.file_path:
                nama_file = os.path.basename(self.file_path)

                folder_tujuan = "file_dokumen"
                if not os.path.exists(folder_tujuan):
                    os.makedirs(folder_tujuan)

                tujuan = os.path.join(folder_tujuan, nama_file)
                shutil.copy(self.file_path, tujuan)

                data[real_index]["file"] = nama_file

            data[real_index]["tanggal"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            simpan_data(data)

            self.app.pop_screen()
            self.app.pop_screen()
            self.app.push_screen(LihatDokumenScreen())


class DeleteScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static("Masukkan nomor dokumen yang ingin dihapus"),
            Input(placeholder="Nomor dokumen", id="nomor"),
            Horizontal(
                Button("Hapus", id="hapus", variant="error"),
                Button("Kembali", id="back"),
            ),
            Static("", id="error"),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()

        elif event.button.id == "hapus":
            nomor_input = self.query_one("#nomor", Input)
            error_text = self.query_one("#error", Static)

            nomor = nomor_input.value.strip()

            if not nomor:
                error_text.update("Nomor harus diisi")
                return

            if not nomor.isdigit():
                error_text.update("Nomor harus berupa angka")
                return

            data = baca_data()
            index = int(nomor)

            if index < 1 or index > len(data):
                error_text.update("Nomor tidak valid")
                return

            data.pop(len(data) - index)
            simpan_data(data)

            self.app.pop_screen()
            self.app.pop_screen()
            self.app.push_screen(LihatDokumenScreen())


def lihat_dokumen(app):
    app.push_screen(LihatDokumenScreen())
