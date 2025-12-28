from perkuliahan.domain.entities.entities import Kelas
from perkuliahan.domain.repositories.repositories import KelasRepository
from perkuliahan.domain.services import IdGeneratorService
from perkuliahan.application.result import Result


class TambahKelasUseCase:
    def __init__(self, repo: KelasRepository, id_gen: IdGeneratorService):
        self.repo = repo
        self.id_gen = id_gen

    def execute(self, nama_kelas: str, id_matakuliah: str, id_dosen: str) -> Result:
        id = self.id_gen.generate_id()
        kelas = Kelas(id=id, nama_kelas=nama_kelas, id_matakuliah=id_matakuliah, id_dosen=id_dosen)
        self.repo.add(kelas)
        return Result.ok()


class UpdateKelasUseCase:
    def __init__(self, repo: KelasRepository):
        self.repo = repo

    def execute(self, id: str, nama_kelas: str, id_matakuliah: str, id_dosen: str) -> Result:
        kelas = Kelas(id=id, nama_kelas=nama_kelas, id_matakuliah=id_matakuliah, id_dosen=id_dosen)
        self.repo.update(kelas)
        return Result.ok()


class DeleteKelasUseCase:
    def __init__(self, repo: KelasRepository):
        self.repo = repo

    def execute(self, id: str) -> Result:
        self.repo.delete_by_id(id)
        return Result.ok()


class DaftarKelasUseCase:
    def __init__(self, repo: KelasRepository):
        self.repo = repo

    def execute(self) -> Result:
        data = self.repo.get_all()
        return Result.ok(data)


class DetailKelasUseCase:
    def __init__(self, repo: KelasRepository):
        self.repo = repo

    def execute(self, id: str) -> Result:
        kelas = self.repo.get_by_id(id)
        if kelas is None:
            return Result.error("Kelas tidak ditemukan")
        return Result.ok(kelas)
    
class CariKelasUseCase:
    def __init__(self, kelas_repository: KelasRepository):
        self.repo = kelas_repository

    def execute(self, keyword: str) -> Result:
        kelas = self.repo.get_by_nama(keyword)
        if kelas is None:
            return Result.error("Kelas tidak ditemukan")
        return Result.ok(kelas)
    
class FilterKelasUseCase:
    def __init__(self, kelas_repository: KelasRepository):
        self.kelas_repository = kelas_repository

    def execute(self, filter: dict) -> Result:
        daftar_kelas = self.kelas_repository.get_by_filter(filter)
        
        # Jika tidak ada hasil, tetap OK tapi kirim list kosong
        if not daftar_kelas:
            return Result.ok([])

        return Result.ok(daftar_kelas)
