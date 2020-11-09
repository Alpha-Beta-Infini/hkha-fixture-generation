import os.path
import sqlite3
import json
import random
import datetime
from random import sample
from datetime import date, timedelta
from math import ceil
from flask import Blueprint, Flask, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.exceptions import abort
import calendar
import holidays
import numpy as np
import pandas as pd
import tempfile


# main = Blueprint('main', __name__)

my_app = Flask(__name__)
if __name__ == '__main__':
    my_app.run()

def get_db_connection():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "hockey.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def get_teams(league):
    conn = get_db_connection()
    # conn = sqlite3.connect('hockey.db')
    # conn.row_factory = sqlite3.Row
    temp = None
    if league == "Men's":
        temp = conn.execute("SELECT * FROM 'teams' WHERE title2='Men''s'")
    elif league == "Women's":
        temp = conn.execute("SELECT * FROM 'teams' WHERE title2='Women''s'")
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


def round_robin(units, sets=None):
    """ Generates a schedule of "fair" pairings from a list of units """
    count = len(units)
    sets = sets or (count - 1)
    half = count // 2
    for turn in range(sets):
        left = units[:half]
        right = units[count - half - 1 + 1:][::-1]
        pairings = list(zip(left, right))
        if turn % 2 == 1:
            pairings = [(y, x) for (x, y) in pairings]
        units.insert(1, units.pop())
        yield pairings


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


@main.route('/timetable', methods=['GET', 'POST'])
def timetable():
    if request.method == 'POST':
        start_date = request.form['startDate']
        start_date_object = date.fromisoformat(start_date)
        hard_end_date = '2021-08-31'
        hard_end_date_object = date.fromisoformat('2021-07-05')
        league = request.form['League']

        teams_json = get_teams(league)
        teams_json_obj = json.loads(teams_json)

        # Premier Division
        premier = []
        for team in teams_json_obj:
            for key, value in team.items():
                if key == 'code':
                    if value == 'Premier':
                        premier.append(team['title'])

        # 1st Division
        first_div = []
        for team in teams_json_obj:
            for key, value in team.items():
                if key == 'code':
                    if value == '1st':
                        first_div.append(team['title'])

        # 2nd Division
        second_div = []
        for team in teams_json_obj:
            for key, value in team.items():
                if key == 'code':
                    if value == '2nd':
                        second_div.append(team['title'])

        # 3rd Division
        third_div = []
        for team in teams_json_obj:
            for key, value in team.items():
                if key == 'code':
                    if value == '3rd':
                        third_div.append(team['title'])

        # 4th Division
        fourth_div = []
        for team in teams_json_obj:
            for key, value in team.items():
                if key == 'code':
                    if value == '4th':
                        fourth_div.append(team['title'])

        # 5th Division
        fifth_div = []
        for team in teams_json_obj:
            for key, value in team.items():
                if key == 'code':
                    if value == '5th':
                        fifth_div.append(team['title'])

        # 6th Division
        sixth_div = []
        for team in teams_json_obj:
            for key, value in team.items():
                if key == 'code':
                    if value == '6th':
                        sixth_div.append(team['title'])

        hk_holidays = holidays.HongKong(years=[2020, 2021])

        hk_holidays_list = []
        for key, value in hk_holidays.items():
            temp = [key, value]
            hk_holidays_list.append(temp[0].isoformat())

        number_of_game_days = np.busday_count(start_date, hard_end_date, weekmask='0000010')

        delta_increment = timedelta(days=7)

        dd = [start_date_object]
        game_date_object = start_date_object
        for i in range(number_of_game_days):
            game_date_object += delta_increment
            dd.append(date.isoformat(game_date_object))

        for game_day in dd:
            if game_day not in hk_holidays_list:
                premier_game_pairings = list(round_robin(premier, sets=(len(premier) * 2 - 2)))
                number_premier_games = len(premier_game_pairings)

                premier_games = {}
                for i, day in enumerate(premier_game_pairings):
                    random.shuffle(day)
                    premier_games[i + 1] = day

                premier_games_df = pd.DataFrame.from_dict(premier_games)

                first_div_pairings = list(round_robin(first_div, sets=(len(first_div) * 2 - 2)))
                number_first_div_games = len(first_div_pairings)

                first_div_games = {}
                for i, day in enumerate(first_div_pairings):
                    random.shuffle(day)
                    first_div_games[i + 1] = day

                first_div_df = pd.DataFrame.from_dict(first_div_games)

                second_div_pairings = list(round_robin(second_div, sets=(len(second_div) * 2 - 2)))
                number_second_div_games = len(second_div_pairings)

                second_div_games = {}
                for i, day in enumerate(second_div_pairings):
                    random.shuffle(day)
                    second_div_games[i + 1] = day

                second_div_df = pd.DataFrame.from_dict(second_div_games)

                third_div_pairings = list(round_robin(third_div, sets=(len(third_div) * 2 - 2)))
                number_third_div_games = len(third_div_pairings)

                third_div_games = {}
                for i, day in enumerate(third_div_pairings):
                    random.shuffle(day)
                    third_div_games[i + 1] = day

                third_div_df = pd.DataFrame.from_dict(third_div_games)

                fourth_div_pairings = list(round_robin(fourth_div, sets=(len(fourth_div) * 2 - 2)))
                number_fourth_div_games = len(fourth_div_pairings)

                fourth_div_games = {}
                for i, day in enumerate(fourth_div_pairings):
                    random.shuffle(day)
                    fourth_div_games[i + 1] = day

                fourth_div_df = pd.DataFrame.from_dict(fourth_div_games)

                fifth_div_pairings = list(round_robin(fifth_div, sets=(len(fifth_div) * 2 - 2)))
                number_fifth_div_games = len(fifth_div_pairings)

                fifth_div_games = {}
                for i, day in enumerate(fifth_div_pairings):
                    random.shuffle(day)
                    fifth_div_games[i + 1] = day

                fifth_div_df = pd.DataFrame.from_dict(fifth_div_games)

                sixth_div_pairings = list(round_robin(sixth_div, sets=(len(sixth_div) * 2 - 2)))
                number_sixth_div_games = len(sixth_div_pairings)

                sixth_div_games = {}
                for i, day in enumerate(sixth_div_pairings):
                    random.shuffle(day)
                    sixth_div_games[i + 1] = day

                sixth_div_df = pd.DataFrame.from_dict(sixth_div_games)

                frames = [premier_games_df, first_div_df, second_div_df, third_div_df, fourth_div_df, fifth_div_df, sixth_div_df]
                all_games_df = pd.concat(frames)

                all_games_df.to_csv('round_1_games.csv',index=False)

        return render_template('timetable.html',
                               start_date=start_date,
                               league=league,
                               premier_games=premier_games,
                               number_premier_games=number_premier_games,
                               first_div_games=first_div_games,
                               number_first_div_games=number_first_div_games,
                               second_div_games=second_div_games,
                               number_second_div_games=number_second_div_games,
                               third_div_games=third_div_games,
                               number_third_div_games=number_third_div_games,
                               fourth_div_games=fourth_div_games,
                               number_fourth_div_games=number_fourth_div_games,
                               fifth_div_games=fifth_div_games,
                               number_fifth_div_games=number_fifth_div_games,
                               sixth_div_games=sixth_div_games,
                               number_sixth_div_games=number_sixth_div_games
                               )
