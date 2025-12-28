# from flask import Flask, render_template, redirect, url_for

# def create_app():
#     app = Flask(__name__)
#     app.config['SECRET_KEY'] = 'mysecretkey'
    
    
#     @app.route("/")
#     def index():
#         return render_template("pages/guests/index.html")
    
#     from .routes import guest_bp, user_bp
    
#     app.register_blueprint(guest_bp)
#     app.register_blueprint(user_bp)
    
#     return app

from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "mysecretkey"
    
    
    from .routes import matakuliah_bp, dosen_bp, mahasiswa_bp, kelas_bp, mk_bp, tugas_bp, penyerahan_bp, penilaian_bp, main_bp, auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(matakuliah_bp)
    app.register_blueprint(dosen_bp)
    app.register_blueprint(mahasiswa_bp)
    app.register_blueprint(kelas_bp)
    app.register_blueprint(mk_bp)
    app.register_blueprint(tugas_bp)
    app.register_blueprint(penyerahan_bp)
    app.register_blueprint(penilaian_bp)
    app.register_blueprint(auth_bp)
    return app