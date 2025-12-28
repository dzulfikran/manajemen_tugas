from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime

class MataKuliah(BaseModel):
    kode_matakuliah: str
    nama_matakuliah: str
    sks: int
    semester: int
    id: str = Field(default=None)
    
class Dosen(BaseModel):
    nidn: str
    nama_dosen: str
    no_hp: str
    alamat: str
    id: str = Field(default=None)

class Mahasiswa(BaseModel):
    nim: str
    nama_mahasiswa: str
    no_hp: str
    alamat: str
    id: str = Field(default=None)

class Kelas(BaseModel):
    nama_kelas: str
    id_matakuliah: str
    id_dosen: str
    id: str = Field(default=None)

class MahasiswaKelas(BaseModel):
    id_mahasiswa: str
    id_kelas: str
    id: str = Field(default=None)

class Tugas(BaseModel):
    nama_tugas: str
    deskripsi: Optional[str] = None
    batas_waktu: datetime
    id_kelas: str
    nama_matakuliah: Optional[str] = None
    status: str = "aktif"
    id: str = Field(default=None)


class PenyerahanTugas(BaseModel):
    id_tugas: str
    waktu_penyerahan: Optional[datetime] = None
    status: str = "belum_dinilai"
    id: str = Field(default=None)


class Penilaian(BaseModel):
    nilai: int
    id_penyerahan: str
    id: str = Field(default=None)
