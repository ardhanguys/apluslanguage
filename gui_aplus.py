import tkinter as tk
from tkinter import filedialog, messagebox
import sys
from aplus import jalankan_code  # Import interpreter kamu

def jalankan_kode():
    kode = editor.get("1.0", tk.END).splitlines()
    global baris_iterator
    baris_iterator = iter(kode)
    output_box.delete("1.0", tk.END)
    sys.stdout = OutputRedirect(output_box)
    try:
        for baris in baris_iterator:
            jalankan_code(baris)
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        sys.stdout = sys.__stdout__

def buka_file():
    path = filedialog.askopenfilename(filetypes=[("A++ Files", "*.aplus")])
    if path:
        with open(path, "r") as f:
            editor.delete("1.0", tk.END)
            editor.insert(tk.END, f.read())

def simpan_file():
    path = filedialog.asksaveasfilename(defaultextension=".aplus", filetypes=[("A++ Files", "*.aplus")])
    if path:
        with open(path, "w") as f:
            f.write(editor.get("1.0", tk.END))

def tampilkan_bantuan():
    """Menampilkan dokumentasi A++ dalam window baru"""
    doc_window = tk.Toplevel(app)
    doc_window.title("Dokumentasi A++")
    doc_window.geometry("600x400")
    
    doc_text = tk.Text(doc_window, wrap="word", height=20, width=60)
    doc_text.pack(padx=10, pady=10)
    
    doc_content = """
    A++ Programming Language - Dokumentasi
    
    1. Input
    - input angka <variabel>: untuk meminta input angka.
    - input <variabel>: untuk meminta input teks.
    
    2. Fungsi
    - buat fungsi <nama_fungsi>(<parameter>):
        Menyusun fungsi dengan parameter.
    - panggil <nama_fungsi>(<argumen>): Memanggil fungsi yang sudah dibuat.
    
    3. Percabangan
    - jika <kondisi> maka:
        Melakukan percabangan berdasarkan kondisi.
    - akhir jika: Mengakhiri percabangan.
    
    4. Perulangan
    - ulangi <jumlah>: Untuk melakukan perulangan.
    - untuk <variabel> dalam <range> sampai <nilai>: Perulangan dengan interval.
    
    5. Variabel
    - isi <variabel> = <nilai>: Untuk mendeklarasikan variabel dengan nilai.
    
    6. Output
    - tulis <pesan>: Menampilkan pesan di output.
    
    7. Error Handling
    - coba: Untuk menangkap error.
    - tangkap: Menampilkan error yang ditangkap.
    """
    
    doc_text.insert(tk.END, doc_content)  # Memasukkan teks ke dalam Text widget
    doc_text.config(state=tk.DISABLED)  # Membuat teks tidak bisa diedit oleh pengguna

class OutputRedirect:
    def __init__(self, textbox):
        self.textbox = textbox

    def write(self, s):
        self.textbox.insert(tk.END, s)
        self.textbox.see(tk.END)

    def flush(self): pass

# ================== GUI ==================
app = tk.Tk()
app.title("A++ IDE V 0.1")
app.geometry("800x600")

frame = tk.Frame(app)
frame.pack(padx=10, pady=10, fill="both", expand=True)

editor = tk.Text(frame, height=20, font=("Courier", 12))
editor.pack(fill="both", expand=True)

btn_frame = tk.Frame(app)
btn_frame.pack()

tk.Button(btn_frame, text="Jalankan", command=jalankan_kode).pack(side="left", padx=5)
tk.Button(btn_frame, text="Buka", command=buka_file).pack(side="left", padx=5)
tk.Button(btn_frame, text="Simpan", command=simpan_file).pack(side="left", padx=5)

# Tombol Bantuan
tk.Button(btn_frame, text="Bantuan", command=tampilkan_bantuan).pack(side="left", padx=5)

output_box = tk.Text(app, height=10, bg="black", fg="lime", font=("Courier", 10))
output_box.pack(fill="x", padx=10, pady=10)

app.mainloop()
