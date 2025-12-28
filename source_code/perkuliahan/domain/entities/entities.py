from dataclasses import dataclass, field

# ------------------------------------------------------
# Mata Kuliah
# ------------------------------------------------------
@dataclass
class MataKuliah:
    id: str
    kode_matakuliah: str
    nama_matakuliah: str
    sks: int
    semester: int
    # Jika ingin menambah deskripsi, bisa tambahkan:
    deskripsi: str | None = None


# ------------------------------------------------------
# Dosen
# ------------------------------------------------------
@dataclass
class Dosen:
    id: str
    nidn: str
    nama_dosen: str
    no_hp: str
    alamat: str | None = None


# ------------------------------------------------------
# Mahasiswa
# ------------------------------------------------------
@dataclass
class Mahasiswa:
    id: str
    nim: str
    nama_mahasiswa: str
    no_hp: str
    alamat: str | None = None


# ------------------------------------------------------
# Kelas
# ------------------------------------------------------
@dataclass
class Kelas:
    id: str
    nama_kelas: str
    id_matakuliah: str
    id_dosen: str


# ------------------------------------------------------
# Relasi Many-to-Many (Mahasiswa -> Kelas)
# ------------------------------------------------------
@dataclass
class MahasiswaKelas:
    id: str
    id_mahasiswa: str
    id_kelas: str
