from abc import ABC, abstractmethod
from perkuliahan.domain.entities import (
    MataKuliah,
    Dosen,
    Mahasiswa,
    Kelas,
    MahasiswaKelas
)

# ------------------------------------------------------
# Base Repository
# ------------------------------------------------------
class BaseRepository(ABC):
    @abstractmethod
    def add(self, entity): pass

    @abstractmethod
    def update(self, entity): pass

    @abstractmethod
    def delete_by_id(self, id: str): pass

    @abstractmethod
    def get_all(self): pass

    @abstractmethod
    def get_by_id(self, id: str): pass


# ------------------------------------------------------
# MataKuliah Repository
# ------------------------------------------------------
class MataKuliahRepository(BaseRepository):

    @abstractmethod
    def get_by_nama_matakuliah(self, nama_matakuliah: str) -> MataKuliah | None:
        pass

    @abstractmethod
    def get_by_keyword(self, keyword: str) -> list[MataKuliah] | None:
        pass

    @abstractmethod
    def get_by_filter(self, filter: dict) -> list[MataKuliah] | None:
        pass


# ------------------------------------------------------
# Dosen Repository
# ------------------------------------------------------
class DosenRepository(BaseRepository):

    @abstractmethod
    def get_by_nidn(self, nidn: str) -> Dosen | None:
        pass

    @abstractmethod
    def get_by_nama_dosen(self, nama_dosen: str) -> list[Dosen] | None:
        pass


# ------------------------------------------------------
# Mahasiswa Repository
# ------------------------------------------------------
class MahasiswaRepository(BaseRepository):

    @abstractmethod
    def get_by_nim(self, nim: str) -> Mahasiswa | None:
        pass

    @abstractmethod
    def get_by_nama_mahasiswa(self, nama_mahasiswa: str) -> list[Mahasiswa] | None:
        pass


# ------------------------------------------------------
# Kelas Repository
# ------------------------------------------------------
class KelasRepository(BaseRepository):

    @abstractmethod
    def get_by_dosen(self, id_dosen: str) -> list[Kelas] | None:
        pass

    @abstractmethod
    def get_by_matakuliah(self, id_matakuliah: str) -> list[Kelas] | None:
        pass

    @abstractmethod
    def get_by_nama_kelas(self, nama_kelas: str) -> list[Kelas] | None:
        pass


# ------------------------------------------------------
# Mahasiswa-Kelas (Many-to-Many)
# ------------------------------------------------------
class MahasiswaKelasRepository(BaseRepository):

    @abstractmethod
    def get_by_mahasiswa(self, id_mahasiswa: str) -> list[MahasiswaKelas] | None:
        pass

    @abstractmethod
    def get_by_kelas(self, id_kelas: str) -> list[MahasiswaKelas] | None:
        pass
