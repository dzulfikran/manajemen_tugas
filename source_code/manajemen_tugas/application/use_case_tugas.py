from ..domain.entities.entities import Tugas
from ..domain.services import IdGeneratorService
from ..domain.repositories.repositories import TugasRepository
from ..application.result import Result
from datetime import datetime

class TambahTugasUseCase:
    def __init__(
        self,
        tugas_repository: TugasRepository,
        id_generator_service: IdGeneratorService,
    ):
        self.tugas_repository = tugas_repository
        self.id_generator_service = id_generator_service

    def execute(
        self, deskripsi: str, nama_tugas: str, batas_waktu: str, nama_matakuliah: str, id_kelas: str
    ) -> Result:
        id = self.id_generator_service.generate_id()
        tugas = Tugas(
            id=id, deskripsi=deskripsi, nama_tugas=nama_tugas, batas_waktu=datetime.fromisoformat(batas_waktu), nama_matakuliah=nama_matakuliah, id_kelas=id_kelas, status="aktif",
        )
        hasil = self.tugas_repository.add(tugas)
        return Result.ok()


class UpdateTugasUseCase:
    def __init__(self, tugas_repository: TugasRepository):
        self.tugas_repository = tugas_repository

    def execute(
        self, id: str, deskripsi: str, nama_tugas: str, batas_waktu: str, nama_matakuliah: str, id_kelas: str
    ) -> Result:
        tugas = Tugas(
            id=id, deskripsi=deskripsi, nama_tugas=nama_tugas, batas_waktu=datetime.fromisoformat(batas_waktu), nama_matakuliah=nama_matakuliah, id_kelas=id_kelas
        )
        hasil = self.tugas_repository.update(tugas)
        return Result.ok()
    
class UpdateStatusInactiveTugasUseCase:
    def __init__(self, tugas_repository: TugasRepository):
        self.tugas_repository = tugas_repository

    def execute(
        self, id: str
    ) -> Result:
        tugas = Tugas(
            id=id
        )
        hasil = self.tugas_repository.update_status_inactive(tugas)
        return Result.ok()
    
class UpdateStatusCompletedTugasUseCase:
    def __init__(self, tugas_repository: TugasRepository):
        self.tugas_repository = tugas_repository

    def execute(
        self, id: str
    ) -> Result:
        tugas = Tugas(
            id=id
        )
        hasil = self.tugas_repository.update_status_completed(tugas)
        return Result.ok()
    
class DeleteTugasUseCase:
    def __init__(self, tugas_repository: TugasRepository):
        self.tugas_repository = tugas_repository

    def execute(self, id: str) -> Result:
        hasil = self.tugas_repository.delete_by_id(id)
        return Result.ok()


class DaftarTugasUseCase:
    def __init__(self, tugas_repository: TugasRepository):
        self.tugas_repository = tugas_repository

    def execute(self) -> Result:
        daftar_tugas = self.tugas_repository.get_all()
        return Result.ok(daftar_tugas)


class DetailTugasUseCase:
    def __init__(self, tugas_repository: TugasRepository):
        self.tugas_repository = tugas_repository

    def execute(self, id: str) -> Result:
        tugas = self.tugas_repository.get_by_id(id)
        if tugas is None:
            return Result.error("Tugas tidak ditemukan")
        return Result.ok(tugas)
    
class CariTugasUseCase:
    def __init__(self, tugas_repository: TugasRepository):
        self.tugas_repository = tugas_repository

    def execute(self, keyword: str) -> Result:
        daftar_tugas = self.tugas_repository.get_by_keyword(keyword)
        if daftar_tugas is None:
            return Result.error("Tugas tidak ditemukan")
        return Result.ok(daftar_tugas)
    
class FilterTugasUseCase:
    def __init__(self, tugas_repository: TugasRepository):
        self.tugas_repository = tugas_repository

    def execute(self, filter: dict) -> Result:
        # validasi level aplikasi
        daftar_tugas = self.tugas_repository.get_by_filter(filter)
        if daftar_tugas is None:
            return Result.error("Tugas tidak ditemukan")
        return Result.ok(daftar_tugas)
