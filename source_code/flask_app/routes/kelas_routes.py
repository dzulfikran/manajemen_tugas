from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..decorators import hx_required

from flask_app.models import Kelas
from flask_app.dto.dto import FilterKelasDTO

from perkuliahan.application.use_case_kelas import (
    DaftarKelasUseCase,
    FilterKelasUseCase,
    TambahKelasUseCase,
    DetailKelasUseCase,
    UpdateKelasUseCase,
    DeleteKelasUseCase,
)

from perkuliahan.infrastructure.sqlite_db.kelas_repository_sqlite import (
    KelasRepositorySqlite,
)
from perkuliahan.infrastructure.uuid.id_services import UuidGeneratorService

kelas_bp = Blueprint("kelas", __name__, url_prefix="/kelas")

@kelas_bp.route("/", methods=["GET"])
def index():
    context = {
        "daftar_kelas": [],
        "params": {},
    }

    params = request.args.to_dict()

    # q → nama_kelas
    if "q" in params and params["q"]:
        params["nama_kelas"] = params["q"]

    dto = FilterKelasDTO(**params)
    context["params"] = dto.model_dump()

    repository = KelasRepositorySqlite()
    filter_data = dto.model_dump(exclude_none=True)

    if not filter_data:
        use_case = DaftarKelasUseCase(repository)
        hasil = use_case.execute()
    else:
        use_case = FilterKelasUseCase(repository)
        hasil = use_case.execute(filter=filter_data)

    if hasil.is_success:
        context["daftar_kelas"] = hasil.data

    # HTMX
    if request.headers.get("HX-Request") == "true":
        return render_template("pages/kelas/list.html", **context)

    return render_template("pages/kelas/index.html", **context)

@kelas_bp.route("/tambah", methods=["GET", "POST"])
def tambah():
    repository = KelasRepositorySqlite()
    id_service = UuidGeneratorService()

    if request.method == "POST":
        kelas = Kelas(
            nama_kelas=request.form["nama_kelas"],
            id_matakuliah=request.form["id_matakuliah"],
            id_dosen=request.form["id_dosen"],
        )

        use_case = TambahKelasUseCase(repository, id_service)
        hasil = use_case.execute(**kelas.model_dump(exclude={"id"}))

        if hasil.is_success:
            flash("Kelas berhasil ditambahkan", "success")
            return redirect(url_for("kelas.index"))
        else:
            flash("Gagal menambahkan kelas", "error")

    return render_template("pages/kelas/tambah.html")

@kelas_bp.route("/<id>/edit", methods=["GET", "POST"])
def edit(id):
    context = {}
    repository = KelasRepositorySqlite()

    # detail kelas
    detail_uc = DetailKelasUseCase(repository)
    hasil_detail = detail_uc.execute(id)

    if not hasil_detail.is_success:
        flash("Data kelas tidak ditemukan", "error")
        return redirect(url_for("kelas.index"))

    context["kelas"] = hasil_detail.data

    if request.method == "POST":
        data = {
            "nama_kelas": request.form.get("nama_kelas"),
            "id_matakuliah": request.form.get("id_matakuliah"),
            "id_dosen": request.form.get("id_dosen"),
        }

        update_uc = UpdateKelasUseCase(repository)
        hasil = update_uc.execute(id=id, **data)

        if hasil.is_success:
            flash("Kelas berhasil diperbarui", "success")
            return redirect(url_for("kelas.index"))
        else:
            flash(hasil.message or "Gagal memperbarui kelas", "error")

    return render_template("pages/kelas/edit.html", **context)

@kelas_bp.route("/<id>/hapus", methods=["POST"])
def hapus(id):
    repository = KelasRepositorySqlite()

    use_case = DeleteKelasUseCase(repository)
    hasil = use_case.execute(id)

    if hasil.is_success:
        flash("Kelas berhasil dihapus", "success")
    else:
        flash(hasil.message or "Gagal menghapus kelas", "error")

    return redirect(url_for("kelas.index"))

from perkuliahan.application.use_case_mahasiswa_kelas import (
    DaftarMahasiswaKelasUseCase,
    TambahMahasiswaKelasUseCase,
    HapusMahasiswaKelasUseCase,
)
from perkuliahan.infrastructure.sqlite_db.mahasiswa_kelas_repository_sqlite import (
    MahasiswaKelasRepositorySqlite,
)

@kelas_bp.route("/<id>/detail", methods=["GET"])
def detail(id):
    context = {"id_kelas": id}

    repo = MahasiswaKelasRepositorySqlite()
    use_case = DaftarMahasiswaKelasUseCase(repo)

    hasil = use_case.execute(id_kelas=id)

    if hasil.is_success:
        context["daftar_mahasiswa"] = hasil.data
    else:
        context["daftar_mahasiswa"] = []

    return render_template("pages/kelas/detail.html", **context)

@kelas_bp.route("/<id_kelas>/tambah-mahasiswa", methods=["POST"])
def tambah_mahasiswa(id_kelas):
    repo = MahasiswaKelasRepositorySqlite()
    id_service = UuidGeneratorService()

    id_mahasiswa = request.form["id_mahasiswa"]

    use_case = TambahMahasiswaKelasUseCase(repo, id_service)
    hasil = use_case.execute(id_mahasiswa=id_mahasiswa, id_kelas=id_kelas)

    if hasil.is_success:
        flash("Mahasiswa berhasil ditambahkan ke kelas", "success")
    else:
        flash("Gagal menambahkan mahasiswa", "error")

    return redirect(url_for("kelas.detail", id=id_kelas))

@kelas_bp.route("/mahasiswa-kelas/<id>/hapus", methods=["POST"])
def hapus_mahasiswa_kelas(id):
    repo = MahasiswaKelasRepositorySqlite()

    use_case = HapusMahasiswaKelasUseCase(repo)
    hasil = use_case.execute(id)

    if hasil.is_success:
        flash("Mahasiswa dikeluarkan dari kelas", "success")
    else:
        flash("Gagal menghapus mahasiswa dari kelas", "error")

    return redirect(request.referrer)
