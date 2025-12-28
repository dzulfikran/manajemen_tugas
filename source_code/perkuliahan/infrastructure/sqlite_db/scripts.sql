PRAGMA foreign_keys = ON;

-- Tabel: matakuliah
CREATE TABLE matakuliah (
    id TEXT PRIMARY KEY,
    kode_matakuliah TEXT,
    nama_matakuliah TEXT,
    sks INTEGER,
    semester TEXT
);

-- Tabel: dosen
CREATE TABLE dosen (
    id TEXT PRIMARY KEY,
    nidn TEXT,
    nama_dosen TEXT,
    no_hp TEXT,
    alamat TEXT
);

-- Tabel: mahasiswa
CREATE TABLE mahasiswa (
    id TEXT PRIMARY KEY,
    nim TEXT,
    nama_mahasiswa TEXT,
    no_hp TEXT,
    alamat TEXT
);

-- Tabel: kelas
CREATE TABLE kelas (
    id TEXT PRIMARY KEY,
    nama_kelas TEXT,
    id_matakuliah TEXT,
    id_dosen TEXT,
    
    FOREIGN KEY (id_matakuliah) REFERENCES matakuliah(id)
        ON DELETE CASCADE ON UPDATE CASCADE,

    FOREIGN KEY (id_dosen) REFERENCES dosen(id)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- Tabel: mahasiswa_kelas (Many-to-Many)
CREATE TABLE mahasiswa_kelas (
    id TEXT PRIMARY KEY,
    id_mahasiswa TEXT,
    id_kelas TEXT,

    FOREIGN KEY (id_mahasiswa) REFERENCES mahasiswa(id)
        ON DELETE CASCADE ON UPDATE CASCADE,

    FOREIGN KEY (id_kelas) REFERENCES kelas(id)
        ON DELETE CASCADE ON UPDATE CASCADE
);
