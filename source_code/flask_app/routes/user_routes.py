from flask import Blueprint, redirect, url_for, render_template, request

user_bp = Blueprint("user_bp", __name__, url_prefix="/users")

@user_bp.route("/dashboard", methods=["GET"])
def dashboard():
    return render_template("pages/users/dashboard.html")

@user_bp.route("/logout", methods=["GET"])
def logout():
   return redirect(url_for(("guest_bp.index")))