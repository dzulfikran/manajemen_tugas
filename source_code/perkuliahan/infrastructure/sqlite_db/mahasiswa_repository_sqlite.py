from ...domain.entities.entities import Mahasiswa
from ...domain.repositories.repositories import MahasiswaRepository
from .db_settings import get_connection
from .mappers import mahasiswa_from_dict


class MahasiswaRepositorySqlite(MahasiswaRepository):
    def __init__(self):
        pass

    def add(self, m: Mahasiswa):
        conn = get_connection()
        cur = conn.cursor()
        sql = """
        INSERT INTO mahasiswa (id, nim, nama_mahasiswa, no_hp, alamat)
        VALUES (?, ?, ?, ?, ?)
        """
        cur.execute(sql, (m.id, m.nim, m.nama_mahasiswa, m.no_hp, m.alamat))
        conn.commit()
        cur.close()
        conn.close()

    def update(self, m: Mahasiswa):
        conn = get_connection()
        cur = conn.cursor()
        sql = """
        UPDATE mahasiswa
        SET nim=?, nama_mahasiswa=?, no_hp=?, alamat=?
        WHERE id=?
        """
        cur.execute(sql, (m.nim, m.nama_mahasiswa, m.no_hp, m.alamat, m.id))
        conn.commit()
        cur.close()
        conn.close()

    def delete_by_id(self, id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM mahasiswa WHERE id=?", (id,))
        conn.commit()
        cur.close()
        conn.close()

    def get_all(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM mahasiswa")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [mahasiswa_from_dict(r) for r in rows]

    def get_by_id(self, id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM mahasiswa WHERE id=?", (id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return mahasiswa_from_dict(row) if row else None

    def get_by_nim(self, nim: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM mahasiswa WHERE nim=?", (nim,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return mahasiswa_from_dict(row) if row else None

    def get_by_nama_mahasiswa(self, nama_mahasiswa: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM mahasiswa WHERE nama_mahasiswa LIKE ?", (f"%{nama_mahasiswa}%",))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [mahasiswa_from_dict(r) for r in rows]
