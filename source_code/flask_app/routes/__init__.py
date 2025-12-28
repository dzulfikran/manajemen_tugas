# from .guest_routes import guest_bp
# from .user_routes import user_bp

# _all_ = ["guest_bp", "user_bp"]

from flask_app.routes.penilaian_routes import penilaian_bp
from .routes import main_bp
from .matakuliah_routes import matakuliah_bp
from .auth_routes import auth_bp
from .dosen_routes import dosen_bp
from .mahasiswa_routes import mahasiswa_bp
from .kelas_routes import kelas_bp
from .mahasiswa_kelas_routes import mk_bp
from .tugas_routes import tugas_bp
from .penilaian_routes import penilaian_bp
from .penyerahan_tugas_routes import penyerahan_bp

__all__ = ["main_bp", "matakuliah_bp", "auth_bp", "dosen_bp", "mahasiswa_bp", "kelas_bp", "mk_bp", "tugas_bp", "penyerahan_bp", "penilaian_bp"]
