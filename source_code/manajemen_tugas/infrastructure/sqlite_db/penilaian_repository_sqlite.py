from ...domain.entities.entities import Penilaian
from ...domain.repositories.repositories import PenilaianRepository
from .db_settings import get_connection
from .mappers import penilaian_to_dict, penilaian_from_dict

class PenilaianRepositorySqlite(PenilaianRepository):
    def __init__(self):
        pass
        
        
    def get_all(self) -> list[Penilaian]:
        koneksi = get_connection()
        cursor = koneksi.cursor()
        sql = "SELECT * FROM penilaian;"
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        koneksi.close()
        
        return [penilaian_from_dict(row) for row in rows]
    
    def get_by_id(self, id: str) -> Penilaian | None:
        koneksi = get_connection()
        cursor = koneksi.cursor()

        cursor.execute(
            "SELECT * FROM penilaian WHERE id = ?;",
            (id,),
        )
        row = cursor.fetchone()

        cursor.close()
        koneksi.close()

        return penilaian_from_dict(row)
    
    def get_by_penyerahan_id(self, id_penyerahan: str) -> Penilaian:
        koneksi = get_connection()
        cursor = koneksi.cursor()

        cursor.execute(
            "SELECT * FROM penilaian WHERE id_penyerahan = ?;",
            (id_penyerahan,)
        )
        row = cursor.fetchone()

        if not row:
            return None

        cursor.close()
        koneksi.close()
        
        return penilaian_from_dict(row)
    
    def add(self, entity: Penilaian) -> None:
        koneksi = get_connection()
        cursor = koneksi.cursor()

        sql = """
            INSERT INTO penilaian
            (id, nilai, id_penyerahan)
            VALUES (?, ?, ?);
        """

        cursor.execute(
            sql,
            (
                entity.id,
                entity.nilai,
                entity.id_penyerahan,
            ),
        )

        koneksi.commit()
        cursor.close()
        koneksi.close()

    def update(self, entity: Penilaian) -> None:
        koneksi = get_connection()
        cursor = koneksi.cursor()

        sql = """
            UPDATE penilaian
            SET nilai = ?, id_penyerahan = ?
            WHERE id = ?;
        """

        cursor.execute(
            sql,
            (
                entity.nilai,
                entity.id_penyerahan,
                entity.id,
            ),
        )

        koneksi.commit()
        cursor.close()
        koneksi.close()

    def delete_by_id(self, id: str) -> None:
        koneksi = get_connection()
        cursor = koneksi.cursor()

        cursor.execute(
            "DELETE FROM penilaian WHERE id = ?;",
            (id,),
        )

        koneksi.commit()
        cursor.close()
        koneksi.close()