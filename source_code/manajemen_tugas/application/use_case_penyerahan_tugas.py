from datetime import datetime
from .result import Result
from ..domain.entities.entities import PenyerahanTugas
from ..domain.repositories.repositories import (
    TugasRepository,
    PenyerahanTugasRepository,
)
from ..domain.services import IdGeneratorService


class BuatPenyerahanTugasUseCase:
    def __init__(
        self,
        penyerahan_repository: PenyerahanTugasRepository,
        id_generator: IdGeneratorService,
    ):
        self.penyerahan_repository = penyerahan_repository
        self.id_generator = id_generator

    def execute(self, id_tugas: str) -> Result:
        penyerahan = PenyerahanTugas(
            id=self.id_generator.generate_id(),
            id_tugas=id_tugas,
            waktu_penyerahan=datetime.now(),
            status="belum_dinilai",
        )

        self.penyerahan_repository.add(penyerahan)
        return Result.ok(penyerahan)
    
class SerahkanTugasUseCase:
    def __init__(
        self,
        tugas_repository: TugasRepository,
        penyerahan_repository: PenyerahanTugasRepository,
        id_generator: IdGeneratorService,
    ):
        self.tugas_repository = tugas_repository
        self.penyerahan_repository = penyerahan_repository
        self.id_generator = id_generator

    def execute(self, id_tugas: str) -> Result:
        # 1️⃣ Cegah submit ulang
        existing = self.penyerahan_repository.get_by_id_tugas(id_tugas)
        if existing:
            return Result.error("Tugas sudah pernah diserahkan")

        # 2️⃣ Update status tugas
        self.tugas_repository.update_status_completed_by_id(id_tugas)

        # 3️⃣ Buat penyerahan
        penyerahan = PenyerahanTugas(
            id=self.id_generator.generate_id(),
            id_tugas=id_tugas,
            waktu_penyerahan=datetime.now(),
            status="belum_dinilai",
        )

        self.penyerahan_repository.add(penyerahan)

        return Result.ok(penyerahan)

# class DaftarPenyerahanTugasUseCase:
#     def __init__(self, repository):
#         self.repository = repository

#     def execute(self):
#         daftar = self.repository.get_all()  # ambil semua penyerahan
#         return Result.ok(daftar)

class DaftarPenyerahanTugasUseCase:
    def __init__(self, penyerahan_tugas_repository: TugasRepository):
        self.penyerahan_tugas_repository = penyerahan_tugas_repository

    def execute(self) -> Result:
        daftar_tugas = self.penyerahan_tugas_repository.get_all()
        return Result.ok(daftar_tugas)

class DetailPenyerahanTugasUseCase:

    def __init__(self, tugas_repo, penyerahan_repo):
        self.tugas_repo = tugas_repo
        self.penyerahan_repo = penyerahan_repo

    def execute(self, id_tugas: str):
        tugas = self.tugas_repo.get_by_id(id_tugas)
        if not tugas:
            return Result.fail("Tugas tidak ditemukan")

        penyerahan = self.penyerahan_repo.get_by_tugas_id(id_tugas)

        return Result.ok({
            "tugas": tugas,
            "penyerahan": penyerahan
        })


class UpdateStatusPenyerahanTugasUseCase:
    def __init__(
        self,
        penyerahan_repository: PenyerahanTugasRepository,
    ):
        self.penyerahan_repository = penyerahan_repository

    def execute(self, id: str, status: str) -> Result:
        if status not in ["belum_dinilai", "dinilai", "perlu_revisi"]:
            return Result.error("Status tidak valid")

        self.penyerahan_repository.update_status(id, status)
        return Result.ok()

class FilterPenyerahanTugasUseCase:
    def __init__(self, penyerah_tugas_repository: PenyerahanTugasRepository):
        self.penyerah_tugas_repository = penyerah_tugas_repository

    def execute(self, filter: dict) -> Result:
        # validasi level aplikasi
        daftar_tugas = self.penyerah_tugas_repository.get_by_filter(filter)
        if daftar_tugas is None:
            return Result.error("Tugas tidak ditemukan")
        return Result.ok(daftar_tugas)
