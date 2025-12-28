CREATE TABLE tugas (
    id TEXT PRIMARY KEY,
    nama_tugas TEXT NOT NULL,
    deskripsi TEXT,
    batas_waktu DATETIME NOT NULL,
    id_kelas TEXT NOT NULL,
    nama_matakuliah TEXT,
    status TEXT DEFAULT 'aktif'
);

CREATE TABLE penyerahan_tugas (
    id TEXT PRIMARY KEY,
    id_tugas TEXT NOT NULL,
    waktu_penyerahan DATETIME,
    status TEXT DEFAULT 'belum_dinilai',

    FOREIGN KEY (id_tugas) REFERENCES tugas(id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE penilaian (
    id TEXT PRIMARY KEY,
    nilai INTEGER NOT NULL,
    id_penyerahan TEXT NOT NULL,

    FOREIGN KEY (id_penyerahan) REFERENCES penyerahan_tugas(id)
        ON DELETE CASCADE ON UPDATE CASCADE
);
