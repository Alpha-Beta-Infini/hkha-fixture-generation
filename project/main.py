import sqlite3
import json
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.exceptions import abort
import calendar
import holidays

main = Blueprint('main', __name__)


def get_db_connection():
    conn = sqlite3.connect('hockey.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_teams(league=None):
    conn = get_db_connection()
    if league == 'MENS':
        temp = conn.execute("SELECT * FROM teams WHERE title2='Men''s'")
        row_headers = [x[0] for x in temp.description]
        teams = temp.fetchall()
        json_data = []
        for team in teams:
            json_data.append(dict(zip(row_headers, team)))
        teams_json = json.dumps(json_data)
        conn.close()
        if teams_json is None:
            abort(404)
        return teams_json


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/scheduler')
@login_required
def scheduler():
    return render_template('scheduler.html')


@main.route('/timetable')
@login_required
def timetable(start_date=None, teams_json=None):
    return render_template('timetable.html')


@main.route('/handle_data', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'POST':
        start_date = request.form['startDate']

        teams_json = get_teams()

        hk_holidays = holidays.HongKong(years=[2020, 2021])

        hk_holidays_list = []

        for key, value in hk_holidays.items():
            temp = [key, value]
            hk_holidays_list.append(temp[0].isoformat())

        return redirect(url_for('main.timetable', start_date=start_date, teams_json=teams_json))
