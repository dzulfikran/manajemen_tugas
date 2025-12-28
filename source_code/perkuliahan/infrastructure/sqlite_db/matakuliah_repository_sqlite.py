from ...domain.entities.entities import MataKuliah
from ...domain.repositories.repositories import MataKuliahRepository
from .db_settings import get_connection
from .mappers import matakuliah_to_dict, matakuliah_from_dict

class MataKuliahRepositorySqlite(MataKuliahRepository):
    def __init__(self):
        pass
        
    def add(self, matakuliah: MataKuliah) -> None:
        koneksi = get_connection()
        cursor = koneksi.cursor()
        sql = "INSERT INTO matakuliah (id, kode_matakuliah, nama_matakuliah, sks, semester) VALUES (?, ?, ?, ?, ?);"
        cursor.execute(sql, (matakuliah.id, matakuliah.kode_matakuliah, matakuliah.nama_matakuliah, matakuliah.sks,  matakuliah.semester))
        koneksi.commit()
        
        cursor.close()
        koneksi.close()
        
    def update(self, matakuliah: MataKuliah) -> None:
        koneksi = get_connection()
        cursor = koneksi.cursor()
        sql = "UPDATE matakuliah SET id = ?, kode_matakuliah = ?, nama_matakuliah = ?, sks = ?, semester = ? WHERE id = ?;"
        cursor.execute(sql, (matakuliah.id, matakuliah.kode_matakuliah, matakuliah.nama_matakuliah, matakuliah.sks, matakuliah.semester, matakuliah.id))
        koneksi.commit()
        
        cursor.close()
        koneksi.close()
        
    def delete_by_id(self, id) -> None:
        koneksi = get_connection()
        cursor = koneksi.cursor()
        sql = "DELETE FROM matakuliah WHERE id = ?;"
        cursor.execute(sql, (id,))
        koneksi.commit()
        
        cursor.close()
        koneksi.close()
        
    def get_all(self) -> list[MataKuliah]:
        koneksi = get_connection()
        cursor = koneksi.cursor()
        sql = "SELECT * FROM matakuliah;"
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        koneksi.close()
        
        return [matakuliah_from_dict(row) for row in rows]
    
    def get_by_id(self, id) -> MataKuliah:
        koneksi = get_connection()
        cursor = koneksi.cursor()
        sql = "SELECT * FROM matakuliah WHERE id = ?;"
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        cursor.close()
        koneksi.close()
        
        return matakuliah_from_dict(row)
    
    def get_by_nama_matakuliah(self, nama_matakuliah):
        koneksi = get_connection()
        cursor = koneksi.cursor()
        sql = "SELECT * FROM matakuliah WHERE nama_matakuliah = ?;"
        cursor.execute(sql, (nama_matakuliah,))
        row = cursor.fetchone()
        cursor.close()
        koneksi.close()
        
        return matakuliah_from_dict(row)
    
    def get_by_keyword(self, keyword) -> list[MataKuliah]:
        koneksi = get_connection()
        cursor = koneksi.cursor()
        sql = "SELECT * FROM matakuliah WHERE nama_matakuliah LIKE ?;"
        cursor.execute(sql, (f"%{keyword}%",))
        rows = cursor.fetchall()
        cursor.close()
        koneksi.close()
        
        return [matakuliah_from_dict(row) for row in rows]
    
    def get_by_filter(self, filter: dict) -> list[MataKuliah]:
        koneksi = get_connection()
        cursor = koneksi.cursor()
        sql = "SELECT * FROM matakuliah WHERE 1 = 1 "
        params = []
        
        # filter nama_matakuliah
        if filter['nama_matakuliah']:
            sql += " AND nama_matakuliah LIKE ?"
            params.append(f"%{filter['nama_matakuliah']}%")
            
        # filter sks
        if filter['sks']:
            sql += " AND sks == ?"
            params.append(filter['sks'])
        
        # filter semester
        if filter['semester']:
            sql += " AND semester == ?"
            params.append(filter['semester'])
        
        
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()
        koneksi.close()
        
        return [matakuliah_from_dict(row) for row in rows]