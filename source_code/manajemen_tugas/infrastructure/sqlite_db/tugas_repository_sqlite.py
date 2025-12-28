from ...domain.entities.entities import Tugas
from ...domain.repositories.repositories import TugasRepository
from .db_settings import get_connection
from .mappers import tugas_to_dict, tugas_from_dict

class TugasRepositorySqlite(TugasRepository):
    def __init__(self):
        pass
        
    def add(self, tugas: Tugas) -> None:
        koneksi = get_connection()
        cursor = koneksi.cursor()
        sql = "INSERT INTO tugas (id, deskripsi, nama_tugas, batas_waktu, nama_matakuliah, id_kelas, status) VALUES (?, ?, ?, ?, ?, ?, ?);"
        cursor.execute(sql, (tugas.id, tugas.deskripsi, tugas.nama_tugas, tugas.batas_waktu,  tugas.nama_matakuliah, tugas.id_kelas, tugas.status))
        koneksi.commit()
        
        cursor.close()
        koneksi.close()
        
    def update(self, tugas: Tugas) -> None:
        koneksi = get_connection()
        cursor = koneksi.cursor()
        sql = "UPDATE tugas SET id = ?, deskripsi = ?, nama_tugas = ?, batas_waktu = ?, nama_matakuliah = ?, id_kelas = ? WHERE id = ?;"
        cursor.execute(sql, (tugas.id, tugas.deskripsi, tugas.nama_tugas, tugas.batas_waktu, tugas.nama_matakuliah, tugas.id_kelas, tugas.id))
        koneksi.commit()
        
        cursor.close()
        koneksi.close()

    def update_status_inactive(self, tugas: Tugas) -> None:
        koneksi = get_connection()
        cursor = koneksi.cursor()
        sql = """
            UPDATE tugas SET status = "tidak aktif"  WHERE id = ?;
        """
        cursor.execute(sql, (tugas.id))
        koneksi.commit()
        
        cursor.close()
        koneksi.close()

    def update_status_completed(self, tugas: Tugas) -> None:
        koneksi = get_connection()
        cursor = koneksi.cursor()
        sql = """
            UPDATE tugas SET status = "selesai"  WHERE id = ?;
        """
        cursor.execute(sql, (tugas.id))
        koneksi.commit()
        
        cursor.close()
        koneksi.close()

    def update_status_completed_by_id(self, id: str) -> None:
        koneksi = get_connection()
        cursor = koneksi.cursor()
        sql = """
            UPDATE tugas SET status = "selesai"  WHERE id = ?;
        """
        cursor.execute(sql, (id,))
        koneksi.commit()
        
        cursor.close()
        koneksi.close()
        
    def delete_by_id(self, id) -> None:
        koneksi = get_connection()
        cursor = koneksi.cursor()
        sql = "DELETE FROM tugas WHERE id = ?;"
        cursor.execute(sql, (id,))
        koneksi.commit()
        
        cursor.close()
        koneksi.close()
        
    def get_all(self) -> list[Tugas]:
        koneksi = get_connection()
        cursor = koneksi.cursor()
        sql = "SELECT * FROM tugas;"
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        koneksi.close()
        
        return [tugas_from_dict(row) for row in rows]
    
    def get_by_id(self, id) -> Tugas:
        koneksi = get_connection()
        cursor = koneksi.cursor()
        sql = "SELECT * FROM tugas WHERE id = ?;"
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        cursor.close()
        koneksi.close()
        
        return tugas_from_dict(row)
    
    def get_by_status(self, status) -> Tugas:
        koneksi = get_connection()
        cursor = koneksi.cursor()
        sql = "SELECT * FROM tugas WHERE status = ?;"
        cursor.execute(sql, (status,))
        row = cursor.fetchone()
        cursor.close()
        koneksi.close()
        
        return tugas_from_dict(row)
    
    def get_by_nama_tugas(self, nama_tugas):
        koneksi = get_connection()
        cursor = koneksi.cursor()
        sql = "SELECT * FROM tugas WHERE nama_tugas = ?;"
        cursor.execute(sql, (nama_tugas,))
        row = cursor.fetchone()
        cursor.close()
        koneksi.close()
        
        return tugas_from_dict(row)
    
    def get_by_keyword(self, keyword) -> list[Tugas]:
        koneksi = get_connection()
        cursor = koneksi.cursor()
        sql = "SELECT * FROM tugas WHERE nama_tugas LIKE ?;"
        cursor.execute(sql, (f"%{keyword}%",))
        rows = cursor.fetchall()
        cursor.close()
        koneksi.close()
        
        return [tugas_from_dict(row) for row in rows]
    
    def get_by_filter(self, filter: dict) -> list[Tugas]:
        koneksi = get_connection()
        cursor = koneksi.cursor()
        sql = "SELECT * FROM tugas WHERE "
        params = []
        
        # # filter nama_tugas
        # if filter['nama_tugas']:
        #     sql += " AND nama_tugas LIKE ?"
        #     params.append(f"%{filter['nama_tugas']}%")
            
        # # filter batas_waktu
        # if filter['batas_waktu']:
        #     sql += " AND batas_waktu == ?"
        #     params.append(filter['batas_waktu'])
        
        # # filter nama_matakuliah
        # if filter['nama_matakuliah']:
        #     sql += " AND nama_matakuliah == ?"
        #     params.append(filter['nama_matakuliah'])

        # filter nama_matakuliah
        if filter['status']:
            sql += " status == ?"
            params.append(filter['status'])
        
        
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()
        koneksi.close()
        
        return [tugas_from_dict(row) for row in rows]