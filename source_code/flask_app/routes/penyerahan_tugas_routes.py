from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_app.dto.dto import FilterPenyerahanTugasDTO, FilterTugasDTO
from datetime import datetime

from manajemen_tugas.application.use_case_penyerahan_tugas import (
    SerahkanTugasUseCase,
    DaftarPenyerahanTugasUseCase,
    DetailPenyerahanTugasUseCase,
    UpdateStatusPenyerahanTugasUseCase,
    FilterPenyerahanTugasUseCase
)

from manajemen_tugas.application.use_case_tugas import (
    FilterTugasUseCase,
    DetailTugasUseCase
)

from manajemen_tugas.infrastructure.sqlite_db.tugas_repository_sqlite import (
    TugasRepositorySqlite,
)

from manajemen_tugas.infrastructure.sqlite_db.penyerahan_tugas_repository_sqlite import (
    PenyerahanTugasRepositorySqlite,
)

from manajemen_tugas.infrastructure.uuid.id_services import (
    UuidGeneratorService,
)

penyerahan_bp = Blueprint(
    "penyerahan",
    __name__,
    url_prefix="/penyerahan"
)

@penyerahan_bp.route("/tugas/<id_tugas>/serahkan", methods=["POST"])
def serahkan_tugas(id_tugas):
    use_case = SerahkanTugasUseCase(
        TugasRepositorySqlite(),
        PenyerahanTugasRepositorySqlite(),
        UuidGeneratorService(),
    )

    hasil = use_case.execute(id_tugas)

    if hasil.is_success:
        flash("Tugas berhasil diserahkan", "success")
    else:
        flash(hasil.message or "Gagal menyerahkan tugas", "error")

    return redirect(request.referrer or url_for("tugas.index"))

@penyerahan_bp.route("/", methods=["GET"])
def index():
    context = {
        "daftar_penyerahan_tugas": [],
        "params": {},
    }

    params = request.args.to_dict()

    # search
    if "q" in params and params["q"]:
        params["status"] = params["q"]

    dto = FilterTugasDTO(**params)
    context["params"] = dto.model_dump()

    repository = PenyerahanTugasRepositorySqlite()
    filter_data = dto.model_dump(exclude_none=True)

    if not filter_data:
        use_case = DaftarPenyerahanTugasUseCase(repository)
        hasil = use_case.execute()
    else:
        use_case = FilterPenyerahanTugasDTO(repository)
        hasil = use_case.execute(filter=filter_data)

    if hasil.is_success:
        daftar = hasil.data

        # Konversi batas_waktu ke datetime
        for tugas in daftar:
            if isinstance(tugas.waktu_penyerahan, str) and tugas.waktu_penyerahan:
                try:
                    tugas.waktu_penyerahan = datetime.fromisoformat(tugas.waktu_penyerahan)
                except ValueError:
                    tugas.waktu_penyerahan = None  # jika format salah

        context["daftar_penyerahan_tugas"] = daftar
    else:
        flash(hasil.message or "Tidak ada tugas yang sudah diserahkan", "error")

    return render_template("pages/penyerahan_tugas/index.html", **context)

# @penyerahan_bp.route("/", methods=["GET"])
# def index():
#     context = {
#         "daftar_penyerahan_tugas": [],
#         "params": {},
#     }

#     # Ambil query params
#     params = request.args.to_dict()

#     # Jika ada pencarian
#     if "q" in params and params["q"]:
#         params["nama_tugas"] = params["q"]

#     # Buat DTO filter
#     dto = FilterTugasDTO(**params)
#     context["params"] = dto.model_dump()

#     repository = TugasRepositorySqlite()
#     filter_data = dto.model_dump(exclude_none=True)

#     # Tambahkan filter status = "selesai"
#     filter_data["status"] = "selesai"

#     # Gunakan use case filter
#     use_case = FilterTugasUseCase(repository)
#     hasil = use_case.execute(filter=filter_data)

#     if hasil.is_success:
#         daftar = hasil.data

#         # Konversi batas_waktu ke datetime
#         for tugas in daftar:
#             if isinstance(tugas.batas_waktu, str) and tugas.batas_waktu:
#                 try:
#                     tugas.batas_waktu = datetime.fromisoformat(tugas.batas_waktu)
#                 except ValueError:
#                     tugas.batas_waktu = None  # jika format salah

#         context["daftar_penyerahan_tugas"] = daftar
#     else:
#         flash(hasil.message or "Tidak ada tugas yang sudah diserahkan", "error")

#     return render_template(
#         "pages/penyerahan_tugas/index.html",
#         **context
#     )

@penyerahan_bp.route("/tugas/<id_tugas>", methods=["GET"])
def daftar_penyerahan(id_tugas):
    use_case = DaftarPenyerahanTugasUseCase(
        PenyerahanTugasRepositorySqlite()
    )

    hasil = use_case.execute(id_tugas)

    if not hasil.is_success:
        flash(hasil.message or "Data penyerahan tidak ditemukan", "error")
        return redirect(url_for("tugas.index"))

    return render_template(
        "pages/penyerahan_tugas/index.html",
        daftar_penyerahan=hasil.data,
        id_tugas=id_tugas,
    )

@penyerahan_bp.route("/<id>", methods=["GET"])
def detail(id):
    tugas_repo = TugasRepositorySqlite()
    penyerahan_repo = PenyerahanTugasRepositorySqlite()

    use_case = DetailPenyerahanTugasUseCase(
        tugas_repo,
        penyerahan_repo
    )

    hasil = use_case.execute(id)

    if not hasil.is_success:
        flash("Tugas tidak ditemukan", "error")
        return redirect(url_for("penyerahan.index"))

    return render_template(
        "pages/penyerahan_tugas/detail.html",
        tugas=hasil.data["tugas"],
        penyerahan=hasil.data["penyerahan"],
    )


@penyerahan_bp.route("/<id>/status", methods=["POST"])
def update_status(id):
    status = request.form.get("status")

    use_case = UpdateStatusPenyerahanTugasUseCase(
        PenyerahanTugasRepositorySqlite()
    )

    hasil = use_case.execute(id, status)

    if hasil.is_success:
        flash("Status penyerahan berhasil diperbarui", "success")
    else:
        flash(hasil.message or "Gagal memperbarui status", "error")

    return redirect(request.referrer or url_for("penyerahan.detail_penyerahan", id=id))
