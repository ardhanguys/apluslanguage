import operator
import math

# ==================== VARIABEL GLOBAL ====================
variabel = {
    "benar": True,
    "salah": False,
    "null": None
}
fungsi = {}
skip = False
dalam_fungsi = False
dalam_kondisi = False
error = None
baris_iterator = None
nama_fungsi = None
blok_fungsi = []

# ==================== OPERATOR & FUNGSI BANTU ====================
ops = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "%": operator.mod,
    "^": operator.pow,
    ">": operator.gt,
    "<": operator.lt,
    "==": operator.eq,
    ">=": operator.ge,
    "<=": operator.le,
    "!=": operator.ne
}

logika = {
    "dan": lambda x, y: x and y,
    "atau": lambda x, y: x or y,
    "tidak": lambda x: not x
}

def konversi_nilai(val):
    if isinstance(val, (int, float, bool, list, dict)) or val is None:
        return val
    try:
        return int(val)
    except:
        try:
            return float(val)
        except:
            val = val.strip()
            if val.lower() == "benar":
                return True
            elif val.lower() == "salah":
                return False
            elif val.lower() == "null":
                return None
            elif val.startswith('"') and val.endswith('"'):
                return val[1:-1]
            else:
                return variabel.get(val, val)

def evaluasi_ekspresi(expr):
    try:
        for var in variabel:
            expr = expr.replace(var, str(variabel[var]))
        expr = expr.replace("^", "**")
        return eval(expr, {"__builtins__": None}, {"math": math})
    except Exception as e:
        return f"[Error: {str(e)}]"

# ==================== FUNGSI UTAMA (PARSER) ====================
def jalankan_code(baris):
    global skip, dalam_fungsi, dalam_kondisi, error, baris_iterator
    global nama_fungsi, blok_fungsi

    baris = baris.strip("\n")
    if not baris or baris.startswith("#"):
        return

    if baris.startswith("input "):
        if skip: return
        bagian = baris[6:].strip()
        if bagian.startswith("angka "):
            nama_var = bagian[6:].strip()
            while True:
                try:
                    nilai = input(f"Masukkan angka untuk {nama_var}: ")
                    variabel[nama_var] = int(nilai)
                    break
                except ValueError:
                    print("Harap masukkan angka!")
        else:
            variabel[bagian] = input(f"Masukkan nilai untuk {bagian}: ")
        return

    elif baris.startswith("buat fungsi "):
        if skip: return
        dalam_fungsi = True
        nama_fungsi = baris[12:].split("(")[0].strip()
        blok_fungsi = []
        return

    elif baris == "akhir fungsi" and dalam_fungsi:
        fungsi[nama_fungsi] = blok_fungsi[:]
        dalam_fungsi = False
        return

    elif dalam_fungsi:
        blok_fungsi.append(baris)
        return

    elif baris.startswith("panggil "):
        if skip: return
        nama = baris[8:].split("(")[0].strip()
        if nama in fungsi:
            for cmd in fungsi[nama]:
                jalankan_code(cmd)
        else:
            print(f"[Error: Fungsi '{nama}' tidak ditemukan]")
        return

    elif baris.startswith("jika "):
        if skip and dalam_kondisi: return
        kondisi = baris[5:].split(" maka")[0].strip()
        skip = not evaluasi_ekspresi(kondisi)
        dalam_kondisi = True
        return

    elif baris == "akhir jika":
        skip = False
        dalam_kondisi = False
        return

    elif baris.startswith("ulangi "):
        if skip: return
        jumlah = int(baris[7:].strip())
        blok = []
        while True:
            next_line = next(baris_iterator, "").rstrip("\n")
            if next_line.strip() == "akhir ulangi":
                break
            blok.append(next_line)
        for _ in range(jumlah):
            for cmd in blok:
                jalankan_code(cmd)
        return

    elif baris.startswith("untuk "):
        if skip: return
        bagian = baris[6:].split(" dalam ")
        var = bagian[0].strip()
        akhir = int(evaluasi_ekspresi(bagian[1].split(" sampai ")[1].strip()))
        blok = []
        while True:
            next_line = next(baris_iterator, "").rstrip("\n")
            if next_line.strip() == "akhir untuk":
                break
            blok.append(next_line)
        for i in range(1, akhir + 1):
            variabel[var] = i
            for cmd in blok:
                jalankan_code(cmd)
        return

    elif baris.startswith("isi "):
        if skip: return
        nama, nilai = baris[4:].split("=", 1)
        nama = nama.strip()
        nilai = nilai.strip()
        if nilai.startswith("[") and nilai.endswith("]"):
            items = nilai[1:-1].split(",")
            variabel[nama] = [konversi_nilai(i.strip()) for i in items]
        elif nilai.startswith("{") and nilai.endswith("}"):
            pairs = nilai[1:-1].split(",")
            variabel[nama] = {}
            for item in pairs:
                k, v = item.split(":", 1)
                variabel[nama][k.strip().strip('"')] = konversi_nilai(v.strip())
        else:
            variabel[nama] = konversi_nilai(evaluasi_ekspresi(nilai))
        return

    elif baris.startswith("tulis "):
        if skip: return
        teks = baris[6:].strip()
        try:
            hasil = evaluasi_ekspresi(teks)
            print(hasil)
        except:
            print(konversi_nilai(teks))
        return

    elif baris == "coba":
        try:
            error = None
        except Exception as e:
            error = str(e)
        return

    elif baris == "tangkap":
        if error:
            print(f"Error: {error}")
            error = None
        return

# ==================== CONTOH PROGRAM ====================
program_contoh = """
# Program demo A++
isi umur = 18
isi buah = ["apel", "mangga", "jeruk"]
isi mahasiswa = {"nama": "Budi", "nilai": 85}

jika umur >= 17 dan umur < 25 maka
    tulis "Anda remaja/dewasa muda"
akhir jika

untuk i dalam 1 sampai 5
    tulis "Perulangan ke-" + i
akhir untuk

tulis "Buah favorit: " + buah[1]
tulis "Nama mahasiswa: " + mahasiswa["nama"]
"""

# ==================== EKSEKUSI PROGRAM ====================
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as f:
            baris_iterator = iter(f.readlines())
    else:
        baris_iterator = iter(program_contoh.strip().split("\n"))

    for baris in baris_iterator:
        jalankan_code(baris)
