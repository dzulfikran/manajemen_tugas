from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_app.models import MahasiswaKelas
from perkuliahan.application.use_case_mahasiswa_kelas import (
    DaftarMahasiswaKelasUseCase,
    TambahMahasiswaKelasUseCase,
    HapusMahasiswaKelasUseCase
)

mk_bp = Blueprint("mahasiswa_kelas", __name__, url_prefix="/mahasiswa_kelas")

@mk_bp.route("/")
def index():
    mk_list = DaftarMahasiswaKelasUseCase().execute()
    if request.headers.get("HX-Request"):
        return render_template("mahasiswa_kelas/_list.html", mk_list=mk_list)
    return render_template("mahasiswa_kelas/index.html", mk_list=mk_list)

@mk_bp.route("/tambah", methods=["GET", "POST"])
def tambah():
    if request.method == "POST":
        data = request.form
        try:
            TambahMahasiswaKelasUseCase().execute(MahasiswaKelas(**data))
            flash("Mahasiswa berhasil ditambahkan ke kelas", "success")
            return redirect(url_for("mahasiswa_kelas.index"))
        except Exception as e:
            flash(str(e), "error")
    return render_template("mahasiswa_kelas/tambah.html")

@mk_bp.route("/<id>/hapus", methods=["POST"])
def hapus(id):
    try:
        HapusMahasiswaKelasUseCase().execute(id)
        flash("Mahasiswa berhasil dihapus dari kelas", "success")
    except Exception as e:
        flash(str(e), "error")
    return redirect(url_for("mahasiswa_kelas.index"))
