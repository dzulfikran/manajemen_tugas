from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..decorators import hx_required

from flask_app.models import Mahasiswa
from flask_app.dto.dto import FilterMahasiswaDTO

from perkuliahan.application.use_case_mahasiswa import (
    DaftarMahasiswaUseCase,
    FilterMahasiswaUseCase,
    TambahMahasiswaUseCase,
    DetailMahasiswaUseCase,
    UpdateMahasiswaUseCase,
    DeleteMahasiswaUseCase,
)

from perkuliahan.infrastructure.sqlite_db.mahasiswa_repository_sqlite import (
    MahasiswaRepositorySqlite,
)
from perkuliahan.infrastructure.uuid.id_services import UuidGeneratorService

mahasiswa_bp = Blueprint("mahasiswa", __name__, url_prefix="/mahasiswa")

@mahasiswa_bp.route("/", methods=["GET"])
def index():
    context = {
        "daftar_mahasiswa": [],
        "params": {},
    }

    params = request.args.to_dict()

    # jika ada q → cari nama_mahasiswa / nim
    if "q" in params and params["q"]:
        params["nama_mahasiswa"] = params["q"]

    dto = FilterMahasiswaDTO(**params)
    context["params"] = dto.model_dump()

    repository = MahasiswaRepositorySqlite()
    filter_data = dto.model_dump(exclude_none=True)

    if not filter_data:
        use_case = DaftarMahasiswaUseCase(repository)
        hasil = use_case.execute()
    else:
        use_case = FilterMahasiswaUseCase(repository)
        hasil = use_case.execute(filter=filter_data)

    if hasil.is_success:
        context["daftar_mahasiswa"] = hasil.data

    # HTMX
    if request.headers.get("HX-Request") == "true":
        return render_template("pages/mahasiswa/list.html", **context)

    return render_template("pages/mahasiswa/index.html", **context)

@mahasiswa_bp.route("/tambah", methods=["GET", "POST"])
def tambah():
    repository = MahasiswaRepositorySqlite()
    id_service = UuidGeneratorService()

    if request.method == "POST":
        mahasiswa = Mahasiswa(
            nim=request.form["nim"],
            nama_mahasiswa=request.form["nama_mahasiswa"],
            no_hp=request.form["no_hp"],
            alamat=request.form["alamat"],
        )

        use_case = TambahMahasiswaUseCase(repository, id_service)
        hasil = use_case.execute(**mahasiswa.model_dump(exclude={"id"}))

        if hasil.is_success:
            flash("Mahasiswa berhasil ditambahkan", "success")
            return redirect(url_for("mahasiswa.index"))
        else:
            flash("Gagal menambahkan mahasiswa", "error")

    return render_template("pages/mahasiswa/tambah.html")

@mahasiswa_bp.route("/<id>/edit", methods=["GET", "POST"])
def edit(id):
    context = {}
    repository = MahasiswaRepositorySqlite()

    # detail mahasiswa
    detail_uc = DetailMahasiswaUseCase(repository)
    hasil_detail = detail_uc.execute(id)

    if not hasil_detail.is_success:
        flash("Data mahasiswa tidak ditemukan", "error")
        return redirect(url_for("mahasiswa.index"))

    context["mahasiswa"] = hasil_detail.data

    if request.method == "POST":
        data = {
            "nim": request.form.get("nim"),
            "nama_mahasiswa": request.form.get("nama_mahasiswa"),
            "no_hp": request.form.get("no_hp"),
            "alamat": request.form.get("alamat"),
        }

        update_uc = UpdateMahasiswaUseCase(repository)
        hasil = update_uc.execute(id=id, **data)

        if hasil.is_success:
            flash("Mahasiswa berhasil diperbarui", "success")
            return redirect(url_for("mahasiswa.index"))
        else:
            flash(hasil.message or "Gagal memperbarui mahasiswa", "error")

    return render_template("pages/mahasiswa/edit.html", **context)

@mahasiswa_bp.route("/<id>/hapus", methods=["POST"])
def hapus(id):
    repository = MahasiswaRepositorySqlite()

    use_case = DeleteMahasiswaUseCase(repository)
    hasil = use_case.execute(id)

    if hasil.is_success:
        flash("Mahasiswa berhasil dihapus", "success")
    else:
        flash(hasil.message or "Gagal menghapus mahasiswa", "error")

    return redirect(url_for("mahasiswa.index"))
