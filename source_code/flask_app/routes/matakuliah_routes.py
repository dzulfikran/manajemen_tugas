from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..decorators import hx_required

from flask_app.models import MataKuliah
from flask_app.dto.dto import FilterMataKuliahDTO

from perkuliahan.application.use_case_matakuliah import (
    DaftarMataKuliahUseCase,
    FilterMataKuliahUseCase,
    TambahMataKuliahUseCase,
    DetailMataKuliahUseCase,
    UpdateMataKuliahUseCase,
    DeleteMataKuliahUseCase,
)

from perkuliahan.infrastructure.sqlite_db.matakuliah_repository_sqlite import (
    MataKuliahRepositorySqlite,
)
from perkuliahan.infrastructure.uuid.id_services import UuidGeneratorService

matakuliah_bp = Blueprint("matakuliah", __name__, url_prefix="/matakuliah")

@matakuliah_bp.route("/", methods=["GET"])
def index():
    context = {
        "daftar_matakuliah": [],
        "params": {},
    }

    params = request.args.to_dict()

    # jika ada q → cari nama_matakuliah
    if "q" in params and params["q"]:
        params["nama_matakuliah"] = params["q"]

    dto = FilterMataKuliahDTO(**params)
    context["params"] = dto.model_dump()

    repository = MataKuliahRepositorySqlite()
    filter_data = dto.model_dump(exclude_none=True)

    if not filter_data:
        use_case = DaftarMataKuliahUseCase(repository)
        hasil = use_case.execute()
    else:
        use_case = FilterMataKuliahUseCase(repository)
        hasil = use_case.execute(filter=filter_data)

    if hasil.is_success:
        context["daftar_matakuliah"] = hasil.data

    # HTMX request
    if request.headers.get("HX-Request") == "true":
        return render_template("pages/matakuliah/list.html", **context)

    return render_template("pages/matakuliah/index.html", **context)

@matakuliah_bp.route("/tambah", methods=["GET", "POST"])
def tambah():
    repository = MataKuliahRepositorySqlite()
    id_service = UuidGeneratorService()

    if request.method == "POST":
        matakuliah = MataKuliah(
            kode_matakuliah=request.form["kode_matakuliah"],
            nama_matakuliah=request.form["nama_matakuliah"],
            sks=int(request.form["sks"]),
            semester=int(request.form["semester"]),
        )

        use_case = TambahMataKuliahUseCase(repository, id_service)
        hasil = use_case.execute(**matakuliah.model_dump(exclude={"id"}))

        if hasil.is_success:
            flash("Mata kuliah berhasil ditambahkan", "success")
            return redirect(url_for("matakuliah.index"))
        else:
            flash("Gagal menambahkan mata kuliah", "error")

    return render_template("pages/matakuliah/tambah.html")

@matakuliah_bp.route("/<id>/edit", methods=["GET", "POST"])
def edit(id):
    context = {}
    repository = MataKuliahRepositorySqlite()

    # detail
    detail_uc = DetailMataKuliahUseCase(repository)
    hasil_detail = detail_uc.execute(id)

    if not hasil_detail.is_success:
        flash("Data mata kuliah tidak ditemukan", "error")
        return redirect(url_for("matakuliah.index"))

    context["matakuliah"] = hasil_detail.data

    if request.method == "POST":
        data = {
            "kode_matakuliah": request.form.get("kode_matakuliah"),
            "nama_matakuliah": request.form.get("nama_matakuliah"),
            "sks": int(request.form.get("sks")),
            "semester": int(request.form.get("semester")),
        }

        update_uc = UpdateMataKuliahUseCase(repository)
        hasil = update_uc.execute(id=id, **data)

        if hasil.is_success:
            flash("Mata kuliah berhasil diperbarui", "success")
            return redirect(url_for("matakuliah.index"))
        else:
            flash(hasil.message or "Gagal memperbarui mata kuliah", "error")

    return render_template("pages/matakuliah/edit.html", **context)

# @matakuliah_bp.route("/<id>/edit", methods=["GET", "POST"])
# def edit(id):
#     context = {}
#     repository = MataKuliahRepositorySqlite()

#     # detail
#     detail_uc = DetailMataKuliahUseCase(repository)
#     hasil_detail = detail_uc.execute(id)

#     if not hasil_detail.is_success:
#         flash("Data mata kuliah tidak ditemukan", "error")
#         return redirect(url_for("matakuliah.index"))

#     context["matakuliah"] = hasil_detail.data

#     if request.method == "POST":
#         data = {
#             "kode_matakuliah": request.form.get("kode_matakuliah"),
#             "nama_matakuliah": request.form.get("nama_matakuliah"),
#             "sks": int(request.form.get("sks")),
#             "deskripsi": request.form.get("deskripsi"),
#             "semester": int(request.form.get("semester")),
#         }

#         update_uc = UpdateMataKuliahUseCase(repository)
#         hasil = update_uc.execute(id=id, **data)

#         if hasil.is_success:
#             flash("Mata kuliah berhasil diperbarui", "success")
#             return redirect(url_for("matakuliah.index"))
#         else:
#             flash(hasil.message or "Gagal memperbarui mata kuliah", "error")

#     return render_template("pages/matakuliah/edit.html", **context)

@matakuliah_bp.route("/<id>/hapus", methods=["POST"])
def hapus(id):
    repository = MataKuliahRepositorySqlite()

    use_case = DeleteMataKuliahUseCase(repository)
    hasil = use_case.execute(id)

    if hasil.is_success:
        flash("Mata kuliah berhasil dihapus", "success")
    else:
        flash(hasil.message or "Gagal menghapus mata kuliah", "error")

    return redirect(url_for("matakuliah.index"))
