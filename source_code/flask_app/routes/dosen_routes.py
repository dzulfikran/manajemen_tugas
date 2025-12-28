from flask import Blueprint, render_template, request, redirect, url_for, flash
from perkuliahan.domain.repositories.repositories import DosenRepository
from perkuliahan.infrastructure.sqlite_db.dosen_repository_sqlite import DosenRepositorySqlite
from ..decorators import hx_required
from flask_app.models import Dosen
from perkuliahan.application.use_case_dosen import (CariDosenUseCase, DaftarDosenUseCase,
    DeleteDosenUseCase, DetailDosenUseCase, FilterDosenUseCase, TambahDosenUseCase,
    UpdateDosenUseCase)
from perkuliahan.infrastructure.uuid.id_services import UuidGeneratorService
from perkuliahan.infrastructure.sqlite_db.dosen_repository_sqlite import (
    DosenRepositorySqlite,
)
from ..utils import validasi
from flask_app.dto.dto import FilterDosenDTO


dosen_bp = Blueprint("dosen", __name__, url_prefix="/dosen")

@dosen_bp.route("/", methods=["GET"])
def index():
    context = {
        "daftar_dosen": [],
        "params": {},
    }

    # ambil semua query string
    params = request.args.to_dict()

    # Jika ada 'q', jadikan filter nama_dosen
    if "q" in params and params["q"]:
        params["nama_dosen"] = params["q"]

    # Simpan params untuk ditampilkan kembali di UI
    dto = FilterDosenDTO(**params)
    context["params"] = dto.model_dump()

    dosen_repository = DosenRepositorySqlite()

    # Ambil field yang tidak None
    filter_data = dto.model_dump(exclude_none=True)

    # Tanpa filter
    if not filter_data:
        use_case = DaftarDosenUseCase(dosen_repository)
        hasil = use_case.execute()
    else:
        # Dengan filter
        use_case = FilterDosenUseCase(dosen_repository)
        hasil = use_case.execute(filter=filter_data)

    if hasil.is_success:
        context["daftar_dosen"] = hasil.data

    # kalau HTMX → render list.html
    if request.headers.get("HX-Request") == "true":
        return render_template("pages/dosen/list.html", **context)

    # page penuh
    return render_template("pages/dosen/index.html", **context)


@dosen_bp.route("/tambah", methods=["GET", "POST"])
def tambah():
    dosen_repository = DosenRepositorySqlite()
    id_service = UuidGeneratorService()

    if request.method == "POST":
        dosen = Dosen(
            nidn=request.form["nidn"],
            nama_dosen=request.form["nama_dosen"],
            alamat=request.form["alamat"],
            no_hp=request.form["no_hp"]
        )
        use_case = TambahDosenUseCase(dosen_repository, id_service)
        hasil = use_case.execute(**dosen.model_dump(exclude={"id"}))

        if hasil.is_success:
            flash("Dosen berhasil ditambahkan", "success")
            return redirect(url_for("dosen.index"))
        else:
            flash("Gagal menambahkan dosen", "error")

    return render_template("pages/dosen/tambah.html")
    # if request.method == "POST":
    #     data = request.form
    #     try:
    #         TambahDosenUseCase().execute(Dosen(**data))
    #         flash("Dosen berhasil ditambahkan", "success")
    #         return redirect(url_for("dosen.index"))
    #     except Exception as e:
    #         flash(str(e), "error")
    
    # return render_template("pages/dosen/tambah.html")

@dosen_bp.route("/<id>/edit", methods=["GET", "POST"])
def edit(id):
    context = {}

    dosen_repository = DosenRepositorySqlite()

    # Ambil data detail dosen
    use_case_detail = DetailDosenUseCase(dosen_repository)
    hasil_detail = use_case_detail.execute(id)

    if not hasil_detail.is_success:
        flash("Data dosen tidak ditemukan", "error")
        return redirect(url_for("dosen.index"))

    # Ambil objek dosen sebenarnya
    dosen = hasil_detail.data
    context["dosen"] = dosen

    # Proses update
    if request.method == "POST":
        data = {
            "nidn": request.form.get("nidn"),
            "nama_dosen": request.form.get("nama_dosen"),
            "no_hp": request.form.get("no_hp"),
            "alamat": request.form.get("alamat"),
        }

        use_case_update = UpdateDosenUseCase(dosen_repository)
        hasil = use_case_update.execute(id=id, **data)

        if hasil.is_success:
            flash("Dosen berhasil diperbarui", "success")
            return redirect(url_for("dosen.index"))
        else:
            flash(hasil.message or "Gagal memperbarui dosen", "error")

    return render_template("pages/dosen/edit.html", **context)


@dosen_bp.route("/<id>/hapus", methods=["POST"])
def hapus(id):
    dosen_repository = DosenRepositorySqlite()

    use_case = DeleteDosenUseCase(dosen_repository)
    hasil = use_case.execute(id)

    if hasil.is_success:
        flash("Dosen berhasil dihapus", "success")
    else:
        flash(hasil.message or "Gagal menghapus dosen", "error")

    return redirect(url_for("dosen.index"))

