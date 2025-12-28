from perkuliahan.domain.entities import MataKuliah, Dosen, Mahasiswa, Kelas, MahasiswaKelas

def matakuliah_to_dict(matakuliah: MataKuliah) -> dict:
    return {
        "id": matakuliah.id,
        "kode_matakuliah": matakuliah.kode_matakuliah,
        "nama_matakuliah": matakuliah.nama_matakuliah,
        "sks": matakuliah.sks,
        "semester": matakuliah.semester
    }
    
def matakuliah_from_dict(matakuliah_dict: dict) -> MataKuliah:
    return MataKuliah(
        id=matakuliah_dict["id"],
        kode_matakuliah=matakuliah_dict["kode_matakuliah"],
        nama_matakuliah=matakuliah_dict["nama_matakuliah"],
        sks=matakuliah_dict["sks"],
        semester=matakuliah_dict["semester"]
    )

def dosen_to_dict(dosen: Dosen) -> dict:
    return {
        "id": dosen.id,
        "nidn": dosen.nidn,
        "nama_dosen": dosen.nama_dosen,
        "alamat": dosen.alamat,
        "no_hp": dosen.no_hp
    }

def dosen_from_dict(d: dict) -> Dosen:
    return Dosen(
        id=d["id"],
        nidn=d["nidn"],
        nama_dosen=d["nama_dosen"],
        alamat=d["alamat"],
        no_hp=d["no_hp"]
    )

def mahasiswa_to_dict(m: Mahasiswa) -> dict:
    return {
        "id": m.id,
        "nim": m.nim,
        "nama_mahasiswa": m.nama_mahasiswa,
        "alamat": m.alamat,
        "no_hp": m.no_hp
    }

def mahasiswa_from_dict(d: dict) -> Mahasiswa:
    return Mahasiswa(
        id=d["id"],
        nim=d["nim"],
        nama_mahasiswa=d["nama_mahasiswa"],
        alamat=d["alamat"],
        no_hp=d["no_hp"]
    )

def kelas_to_dict(k: Kelas) -> dict:
    return {
        "id": k.id,
        "nama_kelas": k.nama_kelas,
        "id_dosen": k.id_dosen,
        "id_matakuliah": k.id_matakuliah
    }

def kelas_from_dict(d: dict) -> Kelas:
    return Kelas(
        id=d["id"],
        nama_kelas=d["nama_kelas"],
        id_dosen=d["id_dosen"],
        id_matakuliah=d["id_matakuliah"]
    )

def mahasiswa_kelas_to_dict(mk: MahasiswaKelas) -> dict:
    return {
        "id": mk.id,
        "id_mahasiswa": mk.id_mahasiswa,
        "id_kelas": mk.id_kelas
    }

def mahasiswa_kelas_from_dict(d: dict) -> MahasiswaKelas:
    return MahasiswaKelas(
        id=d["id"],
        id_mahasiswa=d["id_mahasiswa"],
        id_kelas=d["id_kelas"]
    )