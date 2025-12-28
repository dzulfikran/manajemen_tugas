from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_app.models import Tugas
from flask_app.dto.dto import FilterTugasDTO

from manajemen_tugas.application.use_case_tugas import (
    DaftarTugasUseCase,
    FilterTugasUseCase,
    TambahTugasUseCase,
    DetailTugasUseCase,
    UpdateTugasUseCase,
    DeleteTugasUseCase,
    UpdateStatusCompletedTugasUseCase,
    UpdateStatusInactiveTugasUseCase
)

from manajemen_tugas.application.use_case_penyerahan_tugas import (
    BuatPenyerahanTugasUseCase,
    SerahkanTugasUseCase,
)

from manajemen_tugas.infrastructure.sqlite_db.tugas_repository_sqlite import (
    TugasRepositorySqlite,
)

from manajemen_tugas.infrastructure.sqlite_db.penyerahan_tugas_repository_sqlite import (
    PenyerahanTugasRepositorySqlite,
)

from manajemen_tugas.infrastructure.uuid.id_services import UuidGeneratorService


tugas_bp = Blueprint("tugas", __name__, url_prefix="/tugas")

@tugas_bp.route("/", methods=["GET"])
def index():
    context = {
        "daftar_tugas": [],
        "params": {},
    }

    params = request.args.to_dict()

    # search
    if "q" in params and params["q"]:
        params["nama_tugas"] = params["q"]

    dto = FilterTugasDTO(**params)
    context["params"] = dto.model_dump()

    repository = TugasRepositorySqlite()
    filter_data = dto.model_dump(exclude_none=True)

    if not filter_data:
        use_case = DaftarTugasUseCase(repository)
        hasil = use_case.execute()
    else:
        use_case = FilterTugasUseCase(repository)
        hasil = use_case.execute(filter=filter_data)

    if hasil.is_success:
        context["daftar_tugas"] = hasil.data

    return render_template("pages/tugas/index.html", **context)

@tugas_bp.route("/<id>", methods=["GET"])
def detail(id):
    repository = TugasRepositorySqlite()
    use_case = DetailTugasUseCase(repository)

    hasil = use_case.execute(id)

    if not hasil.is_success:
        flash("Tugas tidak ditemukan", "error")
        return redirect(url_for("tugas.index"))

    return render_template(
        "pages/tugas/detail.html",
        tugas=hasil.data,
    )


@tugas_bp.route("/tambah", methods=["GET", "POST"])
def tambah():
    repository = TugasRepositorySqlite()
    id_service = UuidGeneratorService()

    if request.method == "POST":
        use_case = TambahTugasUseCase(repository, id_service)

        hasil = use_case.execute(
            deskripsi=request.form.get("deskripsi"),
            nama_tugas=request.form["nama_tugas"],
            batas_waktu=request.form["batas_waktu"],
            nama_matakuliah=request.form.get("nama_matakuliah"),
            id_kelas=request.form["id_kelas"],
        )

        if hasil.is_success:
            flash("Tugas berhasil ditambahkan", "success")
            return redirect(url_for("tugas.index"))

        flash(hasil.message or "Gagal menambahkan tugas", "error")

    return render_template("pages/tugas/tambah.html")

@tugas_bp.route("/<id>/edit", methods=["GET", "POST"])
def edit(id):
    repository = TugasRepositorySqlite()

    detail_uc = DetailTugasUseCase(repository)
    hasil_detail = detail_uc.execute(id)

    if not hasil_detail.is_success:
        flash("Tugas tidak ditemukan", "error")
        return redirect(url_for("tugas.index"))

    if request.method == "POST":
        update_uc = UpdateTugasUseCase(repository)
        hasil = update_uc.execute(
            id=id,
            nama_tugas=request.form["nama_tugas"],
            deskripsi=request.form.get("deskripsi"),
            batas_waktu=request.form["batas_waktu"],
            id_kelas=request.form["id_kelas"],
            nama_matakuliah=request.form.get("nama_matakuliah"),
        )

        if hasil.is_success:
            flash("Tugas berhasil diperbarui", "success")
            return redirect(url_for("tugas.index"))

        flash(hasil.message or "Gagal memperbarui tugas", "error")

    return render_template(
        "pages/tugas/edit.html",
        tugas=hasil_detail.data,
    )

@tugas_bp.route("/<id>/hapus", methods=["POST"])
def hapus(id):
    repository = TugasRepositorySqlite()
    use_case = DeleteTugasUseCase(repository)

    hasil = use_case.execute(id)

    if hasil.is_success:
        flash("Tugas berhasil dihapus", "success")
    else:
        flash(hasil.message or "Gagal menghapus tugas", "error")

    return redirect(url_for("tugas.index"))

# @tugas_bp.route("/<id>/serahkan", methods=["POST"])
# def serahkan(id):
#     use_case = SerahkanTugasUseCase(
#         TugasRepositorySqlite(),
#         PenyerahanTugasRepositorySqlite(),
#         IdGeneratorService(),
#     )

#     hasil = use_case.execute(id)

#     if hasil.is_success:
#         flash("Tugas berhasil diserahkan", "success")
#     else:
#         flash(hasil.message or "Gagal menyerahkan tugas", "error")

#     return redirect(url_for("tugas.index"))

