from manajemen_tugas.domain.entities import (
    Tugas, PenyerahanTugas, Penilaian
)
from datetime import datetime

def tugas_to_dict(t: Tugas) -> dict:
    return {
        "id": t.id,
        "nama_tugas": t.nama_tugas,
        "deskripsi": t.deskripsi,
        "batas_waktu": t.batas_waktu,
        "id_kelas": t.id_kelas,
        "nama_matakuliah": t.nama_matakuliah,
        "status": t.status
    }

def tugas_from_dict(d: dict) -> Tugas:
    return Tugas(
        id=d["id"],
        nama_tugas=d["nama_tugas"],
        deskripsi=d["deskripsi"],
        batas_waktu=d["batas_waktu"],
        id_kelas=d["id_kelas"],
        nama_matakuliah=d["nama_matakuliah"],
        status = d["status"] if "status" in d.keys() else "aktif"
    )

def penyerahan_tugas_to_dict(p: PenyerahanTugas) -> dict:
    return {
        "id": p.id,
        "id_tugas": p.id_tugas,
        "waktu_penyerahan": p.waktu_penyerahan,
        "status": p.status
    }

def penyerahan_tugas_from_dict(row) -> PenyerahanTugas:
    if row is None:
        return None

    return PenyerahanTugas(
        id=row["id"],
        id_tugas=row["id_tugas"],
        waktu_penyerahan=datetime.fromisoformat(row["waktu_penyerahan"])
        if row["waktu_penyerahan"] else None,
        status=row["status"],
    )

def penilaian_to_dict(p: Penilaian) -> dict:
    return {
        "id": p.id,
        "nilai": p.nilai,
        "id_penyerahan": p.id_penyerahan
    }

def penilaian_from_dict(d: dict) -> Penilaian:
    return Penilaian(
        id=d["id"],
        nilai=d["nilai"],
        id_penyerahan=d["id_penyerahan"]
    )

