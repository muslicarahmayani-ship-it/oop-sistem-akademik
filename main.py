# ---------------------------------------------------------------
# SISTEM AKADEMIK MINI
# Project OOP Python (Semester 3)
# ---------------------------------------------------------------

from abc import ABC, abstractmethod


# ---------------------------------------------------------------
# EXCEPTION KUSTOM
# ---------------------------------------------------------------
class AkademikError(Exception):
    """Error dasar aplikasi akademik."""


class BatasSksError(AkademikError):
    pass


class DataTidakDitemukanError(AkademikError):
    pass


# ---------------------------------------------------------------
# MATA KULIAH  (Abstract Base Class + Inheritance)
# ---------------------------------------------------------------
class MataKuliah(ABC):
    jumlah_matkul = 0   # class attribute
    JENIS = "Mata Kuliah"

    def __init__(self, kode, nama, sks):
        self.kode = kode
        self.nama = nama
        self.__sks = 0      # private
        self.sks = sks      # lewat setter (ada validasi)
        MataKuliah.jumlah_matkul += 1

    # ----- PROPERTY -----
    @property
    def sks(self):
        return self.__sks

    @sks.setter
    def sks(self, nilai):
        if not 1 <= nilai <= 6:
            raise AkademikError("SKS harus antara 1 sampai 6.")
        self.__sks = nilai

    # ----- CLASS METHOD & STATIC METHOD -----
    @classmethod
    def dapatkan_jumlah(cls):
        return cls.jumlah_matkul

    @staticmethod
    def konversi_huruf(nilai):
        """Ubah nilai angka (0-100) menjadi (huruf, poin)."""
        tabel = [(85, "A", 4.0), (78, "B+", 3.5), (70, "B", 3.0),
                 (65, "C+", 2.5), (55, "C", 2.0), (40, "D", 1.0)]
        for batas, huruf, poin in tabel:
            if nilai >= batas:
                return huruf, poin
        return "E", 0.0

    # ----- ABSTRACT METHOD -----
    @abstractmethod
    def bobot(self):
        """Bobot (tugas, uts, uas) dalam persen. Total harus 100."""

    def hitung_akhir(self, tugas, uts, uas):
        b_tugas, b_uts, b_uas = self.bobot()
        return (tugas * b_tugas + uts * b_uts + uas * b_uas) / 100

    def __str__(self):
        b = self.bobot()
        return (f"[{self.kode}] {self.nama:<24} {self.sks} SKS  {self.JENIS:<9} "
                f"(T{b[0]}/UTS{b[1]}/UAS{b[2]})")


class Teori(MataKuliah):
    JENIS = "Teori"

    def bobot(self):  # polymorphism
        return (20, 30, 50)


class Praktikum(MataKuliah):
    JENIS = "Praktikum"

    def bobot(self):
        return (50, 20, 30)


class Proyek(MataKuliah):
    JENIS = "Proyek"

    def bobot(self):
        return (60, 0, 40)


# ---------------------------------------------------------------
# NILAI  (Composition: menghubungkan Mahasiswa dan MataKuliah)
# ---------------------------------------------------------------
class Nilai:
    KOMPONEN = ("tugas", "uts", "uas")

    def __init__(self, matkul):
        self.matkul = matkul
        self.skor = {k: None for k in self.KOMPONEN}

    def isi(self, komponen, angka):
        if komponen not in self.skor:
            raise AkademikError("Komponen nilai tidak valid.")
        if not 0 <= angka <= 100:
            raise AkademikError("Nilai harus antara 0 sampai 100.")
        self.skor[komponen] = angka

    @property
    def lengkap(self):
        return all(v is not None for v in self.skor.values())

    @property
    def akhir(self):
        if not self.lengkap:
            return None
        return self.matkul.hitung_akhir(self.skor["tugas"], self.skor["uts"], self.skor["uas"])

    @property
    def huruf(self):
        return "-" if self.akhir is None else self.matkul.konversi_huruf(self.akhir)[0]

    @property
    def poin(self):
        return 0.0 if self.akhir is None else self.matkul.konversi_huruf(self.akhir)[1]


# ---------------------------------------------------------------
# MAHASISWA  (Abstract Base Class + Inheritance)
# ---------------------------------------------------------------
class Mahasiswa(ABC):
    JENIS = "Mahasiswa"

    def __init__(self, nim, nama):
        self.nim = nim
        self.nama = nama
        self.krs = []   # composition: daftar Nilai

    # ----- PROPERTY -----
    @property
    def total_sks(self):
        return sum(n.matkul.sks for n in self.krs)

    @property
    def ipk(self):
        """IPK = total (poin x SKS) / total SKS, hanya dari matkul yang nilainya lengkap."""
        selesai = [n for n in self.krs if n.lengkap]
        sks = sum(n.matkul.sks for n in selesai)
        if sks == 0:
            return 0.0
        return sum(n.poin * n.matkul.sks for n in selesai) / sks

    # ----- ABSTRACT METHOD -----
    @abstractmethod
    def batas_sks(self):
        """Batas maksimal SKS yang boleh diambil."""

    @abstractmethod
    def status(self):
        """Status akademik berdasarkan IPK."""

    # ----- METHOD -----
    def cari_nilai(self, kode):
        for n in self.krs:
            if n.matkul.kode == kode:
                return n
        raise DataTidakDitemukanError("Mahasiswa belum mengambil mata kuliah tersebut.")

    def ambil(self, matkul):
        if any(n.matkul.kode == matkul.kode for n in self.krs):
            raise AkademikError(f"{matkul.nama} sudah diambil.")
        if self.total_sks + matkul.sks > self.batas_sks():
            raise BatasSksError(
                f"Melebihi batas SKS ({self.total_sks}+{matkul.sks} > {self.batas_sks()}).")
        nilai = Nilai(matkul)
        self.krs.append(nilai)
        return nilai

    def __len__(self):
        """len(mahasiswa) = jumlah mata kuliah yang diambil."""
        return len(self.krs)

    def __lt__(self, other):
        """Untuk sorted(): dibandingkan berdasarkan IPK."""
        return self.ipk < other.ipk

    def __str__(self):
        return (f"{self.nim} {self.nama:<8} {self.JENIS:<10} {len(self)} matkul / "
                f"{self.total_sks:>2} SKS | IPK {self.ipk:.2f} | {self.status()}")


class Reguler(Mahasiswa):
    JENIS = "Reguler"

    def batas_sks(self):  # polymorphism: bergantung IPK
        return 24 if self.ipk >= 3.0 else 18

    def status(self):
        return "Aman" if self.ipk >= 2.0 or not any(n.lengkap for n in self.krs) else "PERINGATAN akademik"


class Beasiswa(Mahasiswa):
    JENIS = "Beasiswa"
    IPK_MINIMAL = 3.0

    def batas_sks(self):
        return 24   # penerima beasiswa selalu boleh 24 SKS

    def status(self):
        if not any(n.lengkap for n in self.krs) or self.ipk >= self.IPK_MINIMAL:
            return "Aman"
        return f"Beasiswa TERANCAM (IPK < {self.IPK_MINIMAL})"


# ---------------------------------------------------------------
# KAMPUS  (Composition: punya banyak Mahasiswa & MataKuliah)
# ---------------------------------------------------------------
class Kampus:
    JENIS_MAHASISWA = {"1": Reguler, "2": Beasiswa}

    def __init__(self, nama):
        self.nama = nama
        self.mahasiswa = {}
        self.matkul = {}

    def tambah_matkul(self, mk):
        self.matkul[mk.kode] = mk

    def tambah_mahasiswa(self, mhs):
        if mhs.nim in self.mahasiswa:
            raise AkademikError("NIM sudah terdaftar.")
        self.mahasiswa[mhs.nim] = mhs

    def cari_mahasiswa(self, nim):
        mhs = self.mahasiswa.get(nim.strip())
        if mhs is None:
            raise DataTidakDitemukanError("Mahasiswa tidak ditemukan.")
        return mhs

    def cari_matkul(self, kode):
        mk = self.matkul.get(kode.strip().upper())
        if mk is None:
            raise DataTidakDitemukanError("Kode mata kuliah tidak ditemukan.")
        return mk

    def ranking(self):
        return sorted(self.mahasiswa.values(), reverse=True)   # pakai __lt__

    def __len__(self):
        return len(self.mahasiswa)


# ---------------------------------------------------------------
# APLIKASI (menu)
# ---------------------------------------------------------------
class Aplikasi:
    def __init__(self):
        self.kampus = Kampus("Universitas Bina Bangsa")
        self.isi_data_awal()

    def isi_data_awal(self):
        for mk in (Teori("IF201", "Pemrograman Berorientasi Objek", 3),
                   Teori("IF202", "Basis Data", 3),
                   Teori("IF203", "Algoritma dan Struktur Data", 3),
                   Teori("IF204", "Jaringan Komputer", 3),
                   Teori("IF205", "Sistem Operasi", 3),
                   Praktikum("IF211", "Praktikum PBO", 1),
                   Praktikum("IF212", "Praktikum Basis Data", 1),
                   Proyek("IF291", "Proyek Aplikasi", 4)):
            self.kampus.tambah_matkul(mk)
        Tira = Reguler("14012500003", "Tira")
        Rahma = Beasiswa("14012500095", "Rahma")
        self.kampus.tambah_mahasiswa(Tira)
        self.kampus.tambah_mahasiswa(Rahma)
        # contoh nilai awal
        for mhs, nilai in ((Tira, (75, 70, 72)), (Rahma, (95, 90, 92))):
            n = mhs.ambil(self.kampus.cari_matkul("IF201"))
            for komponen, angka in zip(Nilai.KOMPONEN, nilai):
                n.isi(komponen, angka)

    @staticmethod
    def baca_angka(teks):
        try:
            return float(teks.strip().replace(",", "."))
        except ValueError:
            raise AkademikError("Masukkan angka yang valid.")

    def lihat_matkul(self):
        print("\n--- DAFTAR MATA KULIAH ---")
        for mk in self.kampus.matkul.values():
            print(f"  {mk}")

    def daftar_mahasiswa(self):
        nim = input("NIM: ").strip()
        nama = input("Nama: ").strip()
        if not nim or not nama:
            raise AkademikError("NIM dan nama tidak boleh kosong.")
        print("Jenis: 1.Reguler  2.Beasiswa")
        jenis = Kampus.JENIS_MAHASISWA.get(input("Pilihan: ").strip())
        if jenis is None:
            raise AkademikError("Jenis mahasiswa tidak valid.")
        self.kampus.tambah_mahasiswa(jenis(nim, nama))
        print(f"  Mahasiswa {nama} berhasil didaftarkan.")

    def isi_krs(self):
        mhs = self.kampus.cari_mahasiswa(input("NIM: "))
        
        # Ubah daftar matkul ke dalam list berurutan agar memiliki nomor pilihan (indeks)
        daftar_mk = list(self.kampus.matkul.values())
        
        print("\n--- PILIH MATA KULIAH ---")
        for i, mk in enumerate(daftar_mk, start=1):
            print(f"  {i}. {mk}")
            
        pilihan_input = input("Pilih nomor mata kuliah: ").strip()
        
        try:
            indeks = int(pilihan_input) - 1
            if not (0 <= indeks < len(daftar_mk)):
                raise ValueError
            mk = daftar_mk[indeks]
        except ValueError:
            raise AkademikError("Pilihan nomor mata kuliah tidak valid.")
            
        mhs.ambil(mk)
        print(f"  {mhs.nama} mengambil {mk.nama}. Total SKS: {mhs.total_sks}/{mhs.batas_sks()}")

    def input_nilai(self):
        mhs = self.kampus.cari_mahasiswa(input("NIM: "))
        nilai = mhs.cari_nilai(input("Kode mata kuliah: ").strip().upper())
        for komponen in Nilai.KOMPONEN:
            nilai.isi(komponen, self.baca_angka(input(f"  Nilai {komponen.upper()} (0-100): ")))
        print(f"  Nilai akhir: {nilai.akhir:.1f}  ->  Huruf {nilai.huruf} ({nilai.poin})")

    def transkrip(self):
        mhs = self.kampus.cari_mahasiswa(input("NIM: "))
        print(f"\n--- TRANSKRIP {mhs.nama.upper()} ({mhs.nim}) | {mhs.JENIS} ---")
        print(f"  {'Kode':<6} {'Mata Kuliah':<31} SKS  Tugas  UTS  UAS  Akhir  Huruf")
        for n in mhs.krs:
            s = n.skor
            ang = lambda v: f"{v:>5.0f}" if v is not None else "    -"
            akhir = f"{n.akhir:>6.1f}" if n.akhir is not None else "     -"
            print(f"  {n.matkul.kode:<6} {n.matkul.nama:<31} {n.matkul.sks:>3} "
                  f"{ang(s['tugas'])} {ang(s['uts'])} {ang(s['uas'])} {akhir}  {n.huruf:>4}")
        print(f"  Total SKS: {mhs.total_sks}/{mhs.batas_sks()} | IPK: {mhs.ipk:.2f} | Status: {mhs.status()}")

    def ranking(self):
        print("\n--- RANKING IPK ---")
        for urutan, mhs in enumerate(self.kampus.ranking(), start=1):
            print(f"  {urutan}. {mhs}")

    def jalankan(self):
        aksi = {"1": self.lihat_matkul, "2": self.daftar_mahasiswa, "3": self.isi_krs,
                "4": self.input_nilai, "5": self.transkrip, "6": self.ranking}
        while True:
            print(f"\n{'=' * 52}\n SISTEM AKADEMIK - {self.kampus.nama.upper()}\n{'=' * 52}")
            print(" 1. Lihat mata kuliah       4. Input nilai")
            print(" 2. Daftar mahasiswa baru   5. Lihat transkrip")
            print(" 3. Isi KRS                 6. Ranking IPK")
            print(" 0. Keluar")
            pilihan = input("Pilih menu: ").strip()
            if pilihan == "0":
                print(f"\nTerima kasih! Mahasiswa: {len(self.kampus)} | "
                      f"Mata kuliah: {MataKuliah.dapatkan_jumlah()}")
                break
            if pilihan not in aksi:
                print("Menu tidak valid!")
                continue
            try:
                aksi[pilihan]()
            except AkademikError as e:
                print(f"  GAGAL: {e}")


if __name__ == "__main__":
    Aplikasi().jalankan()