# Sistem Akademik Mini

Aplikasi akademik berbasis terminal untuk tugas OOP Python.

**Nama:** (Rahma)  
**NIM:** (14012500095)

## Cara menjalankan
```
python main.py
```

## Data contoh
- Mahasiswa: Tira (NIM 14012500003, Reguler), Rahma (NIM 14012500095, Beasiswa)
- 8 mata kuliah (Teori, Praktikum, Proyek)

## Fitur
- Lihat mata kuliah, daftar mahasiswa baru
- Isi KRS dengan batas SKS
- Input nilai (tugas, UTS, UAS) -> nilai akhir, huruf, IPK otomatis
- Transkrip dan ranking IPK

## Aturan
| Jenis mata kuliah | Bobot Tugas / UTS / UAS |
|---|---|
| Teori | 20 / 30 / 50 |
| Praktikum | 50 / 20 / 30 |
| Proyek | 60 / 0 / 40 |

| Jenis mahasiswa | Batas SKS | Status |
|---|---|---|
| Reguler | 24 jika IPK >= 3.0, selain itu 18 | Peringatan jika IPK < 2.0 |
| Beasiswa | 24 | Terancam jika IPK < 3.0 |

Konversi nilai: A >= 85, B+ >= 78, B >= 70, C+ >= 65, C >= 55, D >= 40, selain itu E.

## Konsep OOP yang digunakan
| Konsep | Contoh di kode |
|---|---|
| Class & Object | `MataKuliah`, `Nilai`, `Mahasiswa`, `Kampus`, `Aplikasi` |
| Encapsulation | `__sks` private |
| Property | `sks` (validasi), `akhir`, `huruf`, `total_sks`, `ipk` |
| Class method | `MataKuliah.dapatkan_jumlah()` |
| Static method | `MataKuliah.konversi_huruf()` |
| Inheritance | `Teori/Praktikum/Proyek(MataKuliah)`, `Reguler/Beasiswa(Mahasiswa)` |
| Polymorphism | `bobot()`, `batas_sks()`, `status()` |
| Abstraction | `MataKuliah(ABC)`, `Mahasiswa(ABC)` |
| Magic method | `__str__`, `__len__`, `__lt__` |
| Composition | `Mahasiswa` punya `Nilai`, `Nilai` punya `MataKuliah` |
| Custom exception | `AkademikError`, `BatasSksError`, `DataTidakDitemukanError` |
