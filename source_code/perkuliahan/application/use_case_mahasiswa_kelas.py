from perkuliahan.domain.entities.entities import MahasiswaKelas
from perkuliahan.domain.repositories.repositories import MahasiswaKelasRepository
from perkuliahan.domain.services import IdGeneratorService
from perkuliahan.application.result import Result


class TambahMahasiswaKelasUseCase:
    def __init__(self, repo: MahasiswaKelasRepository, id_gen: IdGeneratorService):
        self.repo = repo
        self.id_gen = id_gen

    def execute(self, id_mahasiswa: str, id_kelas: str) -> Result:
        id = self.id_gen.generate_id()
        mk = MahasiswaKelas(id=id, id_mahasiswa=id_mahasiswa, id_kelas=id_kelas)
        self.repo.add(mk)
        return Result.ok()


class HapusMahasiswaKelasUseCase:
    def __init__(self, repo: MahasiswaKelasRepository):
        self.repo = repo

    def execute(self, id: str) -> Result:
        self.repo.delete_by_id(id)
        return Result.ok()


class DaftarMahasiswaKelasUseCase:
    def __init__(self, repo: MahasiswaKelasRepository):
        self.repo = repo

    def execute(self, id_kelas: str) -> Result:
        data = self.repo.get_by_kelas(id_kelas)
        return Result.ok(data)
