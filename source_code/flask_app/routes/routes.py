from flask import Blueprint, render_template, redirect, request, url_for, flash, session

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    context = {}

    return render_template("pages/index.html", **context)

