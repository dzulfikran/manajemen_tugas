from ...domain.entities.entities import Dosen
from ...domain.repositories.repositories import DosenRepository
from .db_settings import get_connection
from .mappers import dosen_to_dict, dosen_from_dict


class DosenRepositorySqlite(DosenRepository):
    def __init__(self):
        pass

    def add(self, dosen: Dosen):
        conn = get_connection()
        cur = conn.cursor()
        sql = """
        INSERT INTO dosen (id, nidn, nama_dosen, no_hp, alamat)
        VALUES (?, ?, ?, ?, ?)
        """
        cur.execute(sql, (dosen.id, dosen.nidn, dosen.nama_dosen, dosen.no_hp, dosen.alamat))
        conn.commit()
        cur.close()
        conn.close()

    def update(self, dosen: Dosen):
        conn = get_connection()
        cur = conn.cursor()
        sql = """
        UPDATE dosen SET nidn=?, nama_dosen=?, no_hp=?, alamat=?
        WHERE id=?
        """
        cur.execute(sql, (dosen.nidn, dosen.nama_dosen, dosen.no_hp, dosen.alamat, dosen.id))
        conn.commit()
        cur.close()
        conn.close()

    def delete_by_id(self, id: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM dosen WHERE id=?", (id,))
        conn.commit()
        cur.close()
        conn.close()

    def get_all(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM dosen")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [dosen_from_dict(r) for r in rows]

    def get_by_id(self, id: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM dosen WHERE id=?", (id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return dosen_from_dict(row) if row else None

    def get_by_nidn(self, nidn: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM dosen WHERE nidn=?", (nidn,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return dosen_from_dict(row) if row else None

    def get_by_nama_dosen(self, nama_dosen: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM dosen WHERE nama_dosen LIKE ?", (f"%{nama_dosen}%",))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [dosen_from_dict(r) for r in rows]
