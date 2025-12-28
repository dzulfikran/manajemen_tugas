from perkuliahan.domain.entities.entities import Mahasiswa
from perkuliahan.domain.repositories.repositories import MahasiswaRepository
from perkuliahan.domain.services import IdGeneratorService
from perkuliahan.application.result import Result


class TambahMahasiswaUseCase:
    def __init__(self, repo: MahasiswaRepository, id_gen: IdGeneratorService):
        self.repo = repo
        self.id_gen = id_gen

    def execute(self, nim: str, nama_mahasiswa: str, no_hp: str, alamat: str) -> Result:
        id = self.id_gen.generate_id()
        mhs = Mahasiswa(id=id, nim=nim, nama_mahasiswa=nama_mahasiswa, no_hp=no_hp, alamat=alamat)
        self.repo.add(mhs)
        return Result.ok()


class UpdateMahasiswaUseCase:
    def __init__(self, repo: MahasiswaRepository):
        self.repo = repo

    def execute(self, id: str, nim: str, nama_mahasiswa: str, no_hp: str, alamat: str) -> Result:
        mhs = Mahasiswa(id=id, nim=nim, nama_mahasiswa=nama_mahasiswa, no_hp=no_hp, alamat=alamat)
        self.repo.update(mhs)
        return Result.ok()


class DeleteMahasiswaUseCase:
    def __init__(self, repo: MahasiswaRepository):
        self.repo = repo

    def execute(self, id: str) -> Result:
        self.repo.delete_by_id(id)
        return Result.ok()


class DaftarMahasiswaUseCase:
    def __init__(self, repo: MahasiswaRepository):
        self.repo = repo

    def execute(self) -> Result:
        data = self.repo.get_all()
        return Result.ok(data)


class DetailMahasiswaUseCase:
    def __init__(self, repo: MahasiswaRepository):
        self.repo = repo

    def execute(self, id: str) -> Result:
        mhs = self.repo.get_by_id(id)
        if mhs is None:
            return Result.error("Mahasiswa tidak ditemukan")
        return Result.ok(mhs)


class CariMahasiswaUseCase:
    def __init__(self, repo: MahasiswaRepository):
        self.repo = repo

    def execute(self, keyword: str) -> Result:
        mhs = self.repo.get_by_nama_mahasiswa(keyword)
        if mhs is None:
            return Result.error("Mahasiswa tidak ditemukan")
        return Result.ok(mhs)
    
class FilterMahasiswaUseCase:
    def __init__(self, mahasiswa_repository: MahasiswaRepository):
        self.mahasiswa_repository = mahasiswa_repository

    def execute(self, filter: dict) -> Result:
        daftar_mahasiswa = self.mahasiswa_repository.get_by_filter(filter)
        
        # Jika tidak ada hasil, tetap OK tapi kirim list kosong
        if not daftar_mahasiswa:
            return Result.ok([])

        return Result.ok(daftar_mahasiswa)

