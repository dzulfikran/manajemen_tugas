from perkuliahan.domain.entities.entities import Dosen
from perkuliahan.domain.services import IdGeneratorService
from perkuliahan.domain.repositories.repositories import DosenRepository
from perkuliahan.application.result import Result


class TambahDosenUseCase:
    def __init__(self, dosen_repository: DosenRepository, id_generator: IdGeneratorService):
        self.repo = dosen_repository
        self.id_gen = id_generator

    def execute(self, nidn: str, nama_dosen: str, no_hp: str, alamat: str) -> Result:
        id = self.id_gen.generate_id()
        dosen = Dosen(id=id, nidn=nidn, nama_dosen=nama_dosen, no_hp=no_hp, alamat=alamat)
        
        self.repo.add(dosen)
        return Result.ok(dosen)


class UpdateDosenUseCase:
    def __init__(self, dosen_repository: DosenRepository):
        self.repo = dosen_repository

    def execute(self, id: str, nidn: str, nama_dosen: str, no_hp: str, alamat: str) -> Result:

        existing = self.repo.get_by_id(id)
        if existing is None:
            return Result.error("Dosen tidak ditemukan")

        updated = Dosen(id=id, nidn=nidn, nama_dosen=nama_dosen, no_hp=no_hp, alamat=alamat)
        self.repo.update(updated)

        return Result.ok(updated)


class DeleteDosenUseCase:
    def __init__(self, dosen_repository: DosenRepository):
        self.repo = dosen_repository

    def execute(self, id: str) -> Result:
        existing = self.repo.get_by_id(id)
        if existing is None:
            return Result.error("Dosen tidak ditemukan")

        self.repo.delete_by_id(id)
        return Result.ok()


class DaftarDosenUseCase:
    def __init__(self, dosen_repository: DosenRepository):
        self.repo = dosen_repository

    def execute(self) -> Result:
        data = self.repo.get_all()
        return Result.ok(data)


class DetailDosenUseCase:
    def __init__(self, dosen_repository: DosenRepository):
        self.repo = dosen_repository

    def execute(self, id: str) -> Result:
        dosen = self.repo.get_by_id(id)
        if dosen is None:
            return Result.error("Dosen tidak ditemukan")
        return Result.ok(dosen)


class CariDosenUseCase:
    def __init__(self, dosen_repository: DosenRepository):
        self.repo = dosen_repository

    def execute(self, keyword: str) -> Result:
        daftar = self.repo.search(keyword)  # gunakan LIKE %keyword%

        return Result.ok(daftar)

class FilterDosenUseCase:
    def __init__(self, dosen_repository: DosenRepository):
        self.dosen_repository = dosen_repository

    def execute(self, filter: dict) -> Result:
        daftar_dosen = self.dosen_repository.get_by_filter(filter)
        
        # Jika tidak ada hasil, tetap OK tapi kirim list kosong
        if not daftar_dosen:
            return Result.ok([])

        return Result.ok(daftar_dosen)