from ...domain.entities.entities import PenyerahanTugas
from ...domain.repositories.repositories import PenyerahanTugasRepository
from .db_settings import get_connection
from .mappers import penyerahan_tugas_from_dict
from datetime import datetime

class PenyerahanTugasRepositorySqlite(PenyerahanTugasRepository):
    def __init__(self):
        pass

    # -------------------------
    # BaseRepository
    # -------------------------
    def add(self, entity: PenyerahanTugas) -> None:
        koneksi = get_connection()
        cursor = koneksi.cursor()

        sql = """
            INSERT INTO penyerahan_tugas
            (id, id_tugas, waktu_penyerahan, status)
            VALUES (?, ?, ?, ?);
        """

        cursor.execute(
            sql,
            (
                entity.id,
                entity.id_tugas,
                entity.waktu_penyerahan,
                entity.status,
            ),
        )

        koneksi.commit()
        cursor.close()
        koneksi.close()

    def update(self, entity: PenyerahanTugas) -> None:
        koneksi = get_connection()
        cursor = koneksi.cursor()

        sql = """
            UPDATE penyerahan_tugas
            SET id_tugas = ?, waktu_penyerahan = ?, status = ?
            WHERE id = ?;
        """

        cursor.execute(
            sql,
            (
                entity.id_tugas,
                entity.waktu_penyerahan,
                entity.status,
                entity.id,
            ),
        )

        koneksi.commit()
        cursor.close()
        koneksi.close()

    def update_status_rated_by_id(self, id: str) -> None:
        koneksi = get_connection()
        cursor = koneksi.cursor()
        sql = """
            UPDATE penyerahan_tugas SET status = "dinilai"  WHERE id = ?;
        """
        cursor.execute(sql, (id,))
        koneksi.commit()
        
        cursor.close()
        koneksi.close()

    def delete_by_id(self, id: str) -> None:
        koneksi = get_connection()
        cursor = koneksi.cursor()

        cursor.execute(
            "DELETE FROM penyerahan_tugas WHERE id = ?;",
            (id,),
        )

        koneksi.commit()
        cursor.close()
        koneksi.close()

    def get_all(self) -> list[PenyerahanTugas]:
        koneksi = get_connection()
        cursor = koneksi.cursor()

        cursor.execute("SELECT * FROM penyerahan_tugas;")
        rows = cursor.fetchall()

        cursor.close()
        koneksi.close()

        return [penyerahan_tugas_from_dict(row) for row in rows]

    def get_by_id(self, id: str) -> PenyerahanTugas | None:
        koneksi = get_connection()
        cursor = koneksi.cursor()

        cursor.execute(
            "SELECT * FROM penyerahan_tugas WHERE id = ?;",
            (id,),
        )
        row = cursor.fetchone()

        cursor.close()
        koneksi.close()

        return penyerahan_tugas_from_dict(row)

    # -------------------------
    # PenyerahanTugasRepository
    # -------------------------
    def get_by_status(self, status: str) -> list[PenyerahanTugas]:
        koneksi = get_connection()
        cursor = koneksi.cursor()

        cursor.execute(
            "SELECT * FROM penyerahan_tugas WHERE status = ?;",
            (status,),
        )
        rows = cursor.fetchall()

        cursor.close()
        koneksi.close()

        return [penyerahan_tugas_from_dict(row) for row in rows]

    def get_by_id_tugas(self, id_tugas: str) -> list[PenyerahanTugas]:
        koneksi = get_connection()
        cursor = koneksi.cursor()

        cursor.execute(
            "SELECT * FROM penyerahan_tugas WHERE id_tugas = ?;",
            (id_tugas,),
        )
        rows = cursor.fetchall()

        cursor.close()
        koneksi.close()

        return [penyerahan_tugas_from_dict(row) for row in rows]
    
    def get_by_tugas_id(self, id_tugas: str):
        koneksi = get_connection()
        cursor = koneksi.cursor()

        cursor.execute(
            "SELECT * FROM penyerahan_tugas WHERE id_tugas = ?",
            (id_tugas,)
        )
        row = cursor.fetchone()

        if not row:
            return None
        
        waktu = (
            datetime.fromisoformat(row["waktu_penyerahan"])
            if row["waktu_penyerahan"]
            else None
        )
        
        cursor.close()
        koneksi.close()

        return PenyerahanTugas(
            id=row["id"],
            id_tugas=row["id_tugas"],
            waktu_penyerahan=waktu,
            status=row["status"],
        )
