from abc import ABC, abstractmethod
from manajemen_tugas.domain.entities import (
    Tugas,
    PenyerahanTugas,
    Penilaian
)
from manajemen_tugas.domain.entities.entities import Penilaian, PenyerahanTugas

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
# Tugas
# ------------------------------------------------------
class TugasRepository(BaseRepository):

    @abstractmethod
    def get_by_status(self, status: str) -> list[Tugas] | None:
        pass

    @abstractmethod
    def get_by_nama_tugas(self, nama_tugas: str) -> list[Tugas] | None:
        pass

    @abstractmethod
    def update_status_inactive(self, entity): 
        pass

    @abstractmethod
    def update_status_completed(self, entity): 
        pass

    @abstractmethod
    def update_status_completed_by_id(self, entity): 
        pass

# ------------------------------------------------------
# Penyerahan Tugas
# ------------------------------------------------------
class PenyerahanTugasRepository(BaseRepository):

    @abstractmethod
    def get_by_status(self, status: str) -> list[PenyerahanTugas] | None:
        pass

    @abstractmethod
    def get_by_tugas_id(self, id_tugas: str) -> list[PenyerahanTugas] | None:
        pass

    @abstractmethod
    def get_by_id_tugas(self, id_tugas: str) -> list[PenyerahanTugas] | None:
        pass

    @abstractmethod
    def update_status_rated_by_id(self, entity): 
        pass

# ------------------------------------------------------
# Penilaian
# ------------------------------------------------------
class PenilaianRepository(BaseRepository):

    @abstractmethod
    def get_by_penyerahan_id(self, penyerahan_id: str) -> list[Penilaian] | None:
        pass

    