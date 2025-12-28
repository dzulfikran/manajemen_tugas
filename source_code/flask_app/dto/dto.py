from pydantic import BaseModel

class FilterMataKuliahDTO(BaseModel):
    nama_matakuliah: str | None = None
    sks: str | None = None
    semester: str | None = None
    
    class Config:
        arbitrary_types_allowed = True # untuk mengizinkan tipe data custom
        from_attributes = True

class FilterTugasDTO(BaseModel):
    nama_tugas: str | None = None
    status: str | None = None
    
    class Config:
        arbitrary_types_allowed = True # untuk mengizinkan tipe data custom
        from_attributes = True

class FilterPenyerahanTugasDTO(BaseModel):
    status: str | None = None
    
    class Config:
        arbitrary_types_allowed = True # untuk mengizinkan tipe data custom
        from_attributes = True

class FilterPenilaianDTO(BaseModel):
    nilai: str | None = None
    
    class Config:
        arbitrary_types_allowed = True # untuk mengizinkan tipe data custom
        from_attributes = True

class FilterDosenDTO(BaseModel):
    nama_dosen: str | None = None
    alamat: str | None = None
    
    class Config:
        arbitrary_types_allowed = True # untuk mengizinkan tipe data custom
        from_attributes = True

class FilterMahasiswaDTO(BaseModel):
    nama_mahasiswa: str | None = None
    alamat: str | None = None
    
    class Config:
        arbitrary_types_allowed = True # untuk mengizinkan tipe data custom
        from_attributes = True

class FilterKelasDTO(BaseModel):
    nama_kelas: str | None = None
    
    class Config:
        arbitrary_types_allowed = True # untuk mengizinkan tipe data custom
        from_attributes = True