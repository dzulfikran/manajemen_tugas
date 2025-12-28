from perkuliahan.domain.entities.entities import MataKuliah
from perkuliahan.domain.services import IdGeneratorService
from perkuliahan.domain.repositories.repositories import MataKuliahRepository
from perkuliahan.application.result import Result


class TambahMataKuliahUseCase:
    def __init__(
        self,
        matakuliah_repository: MataKuliahRepository,
        id_generator_service: IdGeneratorService,
    ):
        self.matakuliah_repository = matakuliah_repository
        self.id_generator_service = id_generator_service

    def execute(
        self, kode_matakuliah: str, nama_matakuliah: str, sks: str, semester: str
    ) -> Result:
        id = self.id_generator_service.generate_id()
        matakuliah = MataKuliah(
            id=id, kode_matakuliah=kode_matakuliah, nama_matakuliah=nama_matakuliah, sks=sks, semester=semester
        )
        hasil = self.matakuliah_repository.add(matakuliah)
        return Result.ok()


class UpdateMataKuliahUseCase:
    def __init__(self, matakuliah_repository: MataKuliahRepository):
        self.matakuliah_repository = matakuliah_repository

    def execute(
        self, id: str, kode_matakuliah: str, nama_matakuliah: str, sks: str, semester: str
    ) -> Result:
        matakuliah = MataKuliah(
            id=id, kode_matakuliah=kode_matakuliah, nama_matakuliah=nama_matakuliah, sks=sks, semester=semester
        )
        hasil = self.matakuliah_repository.update(matakuliah)
        return Result.ok()
    
class DeleteMataKuliahUseCase:
    def __init__(self, matakuliah_repository: MataKuliahRepository):
        self.matakuliah_repository = matakuliah_repository

    def execute(self, id: str) -> Result:
        hasil = self.matakuliah_repository.delete_by_id(id)
        return Result.ok()


class DaftarMataKuliahUseCase:
    def __init__(self, matakuliah_repository: MataKuliahRepository):
        self.matakuliah_repository = matakuliah_repository

    def execute(self) -> Result:
        daftar_matakuliah = self.matakuliah_repository.get_all()
        return Result.ok(daftar_matakuliah)


class DetailMataKuliahUseCase:
    def __init__(self, matakuliah_repository: MataKuliahRepository):
        self.matakuliah_repository = matakuliah_repository

    def execute(self, id: str) -> Result:
        matakuliah = self.matakuliah_repository.get_by_id(id)
        if matakuliah is None:
            return Result.error("Mata Kuliah tidak ditemukan")
        return Result.ok(matakuliah)
    
class CariMataKuliahUseCase:
    def __init__(self, matakuliah_repository: MataKuliahRepository):
        self.matakuliah_repository = matakuliah_repository

    def execute(self, keyword: str) -> Result:
        daftar_matakuliah = self.matakuliah_repository.get_by_keyword(keyword)
        if daftar_matakuliah is None:
            return Result.error("Mata Kuliah tidak ditemukan")
        return Result.ok(daftar_matakuliah)
    
class FilterMataKuliahUseCase:
    def __init__(self, matakuliah_repository: MataKuliahRepository):
        self.matakuliah_repository = matakuliah_repository

    def execute(self, filter: dict) -> Result:
        # validasi level aplikasi
        daftar_matakuliah = self.matakuliah_repository.get_by_filter(filter)
        if daftar_matakuliah is None:
            return Result.error("MataKuliah tidak ditemukan")
        return Result.ok(daftar_matakuliah)
