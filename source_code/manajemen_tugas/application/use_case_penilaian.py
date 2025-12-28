from datetime import datetime
from .result import Result
from ..domain.entities.entities import PenyerahanTugas, Penilaian
from ..domain.repositories.repositories import (
    TugasRepository,
    PenyerahanTugasRepository,
    PenilaianRepository,
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
    
class DetailFormPenilaianUseCase:

    def __init__(self, penilaian_repo):
        self.penilaian_repo = penilaian_repo

    def execute(self, id_penyerahan: str):
        penilaian = self.penilaian_repo.get_by_penyerahan_id(id_penyerahan)
        return Result.ok(penilaian)
    
class BeriNilaiUseCase:
    def __init__(
        self,
        penyerahan_repository: PenyerahanTugasRepository,
        penilaian_repository: PenilaianRepository,
        id_generator: IdGeneratorService,
    ):
        self.penyerahan_repository = penyerahan_repository
        self.penilaian_repository = penilaian_repository
        self.id_generator = id_generator

    def execute(self, id_penyerahan: str, nilai: str) -> Result:
        # 1️⃣ Cegah submit ulang
        existing = self.penilaian_repository.get_by_penyerahan_id(id_penyerahan)
        if existing:
            return Result.error("Tugas sudah pernah diberi nilai")

        # 2️⃣ Update status penyerahan tugas
        self.penyerahan_repository.update_status_rated_by_id(id_penyerahan)

        # 3️⃣ Buat Penilaian
        penilaian = Penilaian(
            id=self.id_generator.generate_id(),
            nilai=nilai,
            id_penyerahan=id_penyerahan,
        )

        self.penilaian_repository.add(penilaian)

        return Result.ok(penilaian)

# class DaftarPenyerahanTugasUseCase:
#     def __init__(self, repository):
#         self.repository = repository

#     def execute(self):
#         daftar = self.repository.get_all()  # ambil semua penyerahan
#         return Result.ok(daftar)

class DaftarPenilaianUseCase:
    def __init__(self, penilaian_repository: PenilaianRepository):
        self.penilaian_repository = penilaian_repository

    def execute(self) -> Result:
        daftar_penilaian = self.penilaian_repository.get_all()
        return Result.ok(daftar_penilaian)

class DetailPenilaianUseCase:
    def __init__(self, penyerahan_repo, penilaian_repo, tugas_repo):
        self.penyerahan_repo = penyerahan_repo
        self.penilaian_repo = penilaian_repo
        self.tugas_repo = tugas_repo

    def execute(self, id_penyerahan: str):
        penyerahan = self.penyerahan_repo.get_by_id(id_penyerahan)
        if not penyerahan:
            return Result.fail("Penyerahan tugas tidak ditemukan")

        tugas = self.tugas_repo.get_by_id(penyerahan.id_tugas)
        if not tugas:
            return Result.fail("Tugas tidak ditemukan")

        penilaian = self.penilaian_repo.get_by_penyerahan_id(id_penyerahan)

        return Result.ok({
            "tugas": tugas,
            "penyerahan": penyerahan,
            "penilaian": penilaian
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
        daftar_penilaian = self.penyerah_tugas_repository.get_by_filter(filter)
        if daftar_penilaian is None:
            return Result.error("Tugas tidak ditemukan")
        return Result.ok(daftar_penilaian)
