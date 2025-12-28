from ...domain.entities.entities import MahasiswaKelas
from ...domain.repositories.repositories import MahasiswaKelasRepository
from .db_settings import get_connection
from .mappers import mahasiswa_kelas_from_dict


class MahasiswaKelasRepositorySqlite(MahasiswaKelasRepository):
    def __init__(self):
        pass

    def add(self, mk: MahasiswaKelas):
        conn = get_connection()
        cur = conn.cursor()
        sql = """
        INSERT INTO mahasiswa_kelas (id, id_mahasiswa, id_kelas)
        VALUES (?, ?, ?)
        """
        cur.execute(sql, (mk.id, mk.id_mahasiswa, mk.id_kelas))
        conn.commit()
        cur.close()
        conn.close()

    def update(self, mk: MahasiswaKelas):
        conn = get_connection()
        cur = conn.cursor()
        sql = """
        UPDATE mahasiswa_kelas
        SET id_mahasiswa=?, id_kelas=?
        WHERE id=?
        """
        cur.execute(sql, (mk.id_mahasiswa, mk.id_kelas, mk.id))
        conn.commit()
        cur.close()
        conn.close()

    def delete_by_id(self, id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM mahasiswa_kelas WHERE id=?", (id,))
        conn.commit()
        cur.close()
        conn.close()

    def get_all(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM mahasiswa_kelas")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [mahasiswa_kelas_from_dict(r) for r in rows]

    def get_by_id(self, id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM mahasiswa_kelas WHERE id=?", (id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return mahasiswa_kelas_from_dict(row) if row else None

    def get_by_mahasiswa(self, id_mahasiswa: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM mahasiswa_kelas WHERE id_mahasiswa=?", (id_mahasiswa,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [mahasiswa_kelas_from_dict(r) for r in rows]

    def get_by_kelas(self, id_kelas: str):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM mahasiswa_kelas WHERE id_kelas=?", (id_kelas,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [mahasiswa_kelas_from_dict(r) for r in rows]
