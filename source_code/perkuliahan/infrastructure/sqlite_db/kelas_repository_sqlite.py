from ...domain.entities.entities import Kelas
from ...domain.repositories.repositories import KelasRepository
from .db_settings import get_connection
from .mappers import kelas_from_dict


class KelasRepositorySqlite(KelasRepository):
    def __init__(self):
        pass

    def add(self, kelas: Kelas):
        conn = get_connection()
        cur = conn.cursor()
        sql = """
        INSERT INTO kelas (id, nama_kelas, id_dosen, id_matakuliah)
        VALUES (?, ?, ?, ?)
        """
        cur.execute(sql, (kelas.id, kelas.nama_kelas, kelas.id_dosen, kelas.id_matakuliah))
        conn.commit()
        cur.close()
        conn.close()

    def update(self, kelas: Kelas):
        conn = get_connection()
        cur = conn.cursor()
        sql = """
        UPDATE kelas
        SET nama_kelas=?, id_dosen=?, id_matakuliah=?
        WHERE id=?
        """
        cur.execute(sql, (kelas.nama_kelas, kelas.id_dosen, kelas.id_matakuliah, kelas.id))
        conn.commit()
        cur.close()
        conn.close()

    def delete_by_id(self, id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM kelas WHERE id=?", (id,))
        conn.commit()
        cur.close()
        conn.close()

    def get_all(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM kelas")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [kelas_from_dict(r) for r in rows]

    def get_by_id(self, id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM kelas WHERE id=?", (id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return kelas_from_dict(row) if row else None

    def get_by_dosen(self, id_dosen: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM kelas WHERE id_dosen=?", (id_dosen,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [kelas_from_dict(r) for r in rows]

    def get_by_matakuliah(self, id_matakuliah: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM kelas WHERE id_matakuliah=?", (id_matakuliah,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [kelas_from_dict(r) for r in rows]

    def get_by_nama_kelas(self, nama_kelas: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM kelas WHERE nama_kelas LIKE ?", (f"%{nama_kelas}%",))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [kelas_from_dict(r) for r in rows]
