from flask import Blueprint, redirect, url_for, render_template, request

guest_bp = Blueprint("guest_bp", __name__, url_prefix="/guest")

@guest_bp.route("/", methods=["GET"])
def index():
    return render_template("pages/guests/index.html")

@guest_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect(url_for("user_bp.dashboard"))
    return render_template("pages/guests/login.html")

@guest_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        return redirect(url_for("user_bp.dashboard"))
    return render_template("pages/guests/register.html")