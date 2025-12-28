from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_app.dto.dto import FilterPenyerahanTugasDTO, FilterTugasDTO, FilterPenilaianDTO
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

from flask import Blueprint, render_template, request, redirect, url_for, flash

from manajemen_tugas.infrastructure.sqlite_db.penilaian_repository_sqlite import PenilaianRepositorySqlite
from manajemen_tugas.application.use_case_penilaian import BeriNilaiUseCase, DetailFormPenilaianUseCase, DaftarPenilaianUseCase, DetailPenilaianUseCase

penilaian_bp = Blueprint("penilaian", __name__, url_prefix="/penilaian")


@penilaian_bp.route("/<id_penyerahan>/form", methods=["GET"])
def form(id_penyerahan):
    use_case = DetailFormPenilaianUseCase(
        PenilaianRepositorySqlite()
    )

    hasil = use_case.execute(id_penyerahan)

    if not hasil.is_success:
        flash("Data penilaian tidak ditemukan", "error")
        return redirect(request.referrer or url_for("penyerahan.index"))

    return render_template(
        "pages/penilaian/form.html",
        id_penyerahan=id_penyerahan,
        penilaian=hasil.data
    )


@penilaian_bp.route("/<id_penyerahan>/simpan", methods=["POST"])
def simpan(id_penyerahan):
    nilai = int(request.form.get("nilai"))

    use_case = BeriNilaiUseCase(
        PenyerahanTugasRepositorySqlite(),
        PenilaianRepositorySqlite(),
        UuidGeneratorService(),
    )

    hasil = use_case.execute(id_penyerahan, nilai)

    if hasil.is_success:
        flash("Nilai berhasil disimpan", "success")
    else:
        flash("Gagal menyimpan nilai")

    return redirect(url_for("penyerahan.index"))

@penilaian_bp.route("/", methods=["GET"])
def index():
    context = {
        "daftar_penilaian": [],
        "params": {},
    }

    params = request.args.to_dict()

    # search
    if "q" in params and params["q"]:
        params["nilai"] = params["q"]

    dto = FilterPenilaianDTO(**params)
    context["params"] = dto.model_dump()

    penilaian_repo = PenilaianRepositorySqlite()
    penyerahan_repo = PenyerahanTugasRepositorySqlite()
    filter_data = dto.model_dump(exclude_none=True)

    # Ambil daftar penilaian
    if not filter_data:
        use_case = DaftarPenilaianUseCase(penilaian_repo)
        hasil = use_case.execute()
    else:
        use_case = FilterPenilaianDTO(penilaian_repo)
        hasil = use_case.execute(filter=filter_data)

    if hasil.is_success:
        daftar = hasil.data

        # Tambahkan id_tugas dari penyerahan
        for p in daftar:
            penyerahan = penyerahan_repo.get_by_id(p.id_penyerahan)
            if penyerahan:
                p.id_tugas = penyerahan.id_tugas
            else:
                p.id_tugas = None

        context["daftar_penilaian"] = daftar

    return render_template("pages/penilaian/index.html", **context)

@penilaian_bp.route("/<id_penyerahan>", methods=["GET"])
def detail(id_penyerahan):
    use_case = DetailPenilaianUseCase(
        PenyerahanTugasRepositorySqlite(),
        PenilaianRepositorySqlite(),
        TugasRepositorySqlite()
    )
    hasil = use_case.execute(id_penyerahan)

    if not hasil.is_success:
        flash(hasil.message or "Data tidak ditemukan", "error")
        return redirect(url_for("penilaian.index"))

    return render_template(
        "pages/penilaian/detail.html",
        tugas=hasil.data["tugas"],
        penyerahan=hasil.data["penyerahan"],
        penilaian=hasil.data["penilaian"],
    )




@penilaian_bp.route("/<id>/status", methods=["POST"])
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
