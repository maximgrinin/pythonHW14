from flask import Flask, jsonify
from utils import get_by_title, get_by_period, get_by_rating, get_by_genre

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
# app.json.ensure_ascii = False


# Вьюшка для фильма по названию/части названия
@app.route("/movie/<title>")
def page_movie_by_title(title):
    movie = get_by_title(title)

    return jsonify(movie)


# Вьюшка для фильмов по интервалу лет
@app.route("/movie/<int:year_start>/to/<int:year_end>")
def page_year_to_year(year_start, year_end):
    movies_list = get_by_period(year_start, year_end)

    return jsonify(movies_list)


# Вьюшка для фильмов с детским рейтингом
@app.route("/rating/children/")
def page_rating_children():
    movies_list = get_by_rating('children')

    return jsonify(movies_list)


# Вьюшка для фильмов с семейным рейтингом
@app.route("/rating/family/")
def page_rating_family():
    movies_list = get_by_rating('family')

    return jsonify(movies_list)


# Вьюшка для фильмов со взрослым рейтингом
@app.route("/rating/adult/")
def page_rating_adult():
    movies_list = get_by_rating('adult')

    return jsonify(movies_list)


# Вьюшка для фильмов по жанру
@app.route("/genre/<genre>")
def page_movie_by_genre(genre):
    movies_list = get_by_genre(genre)

    return jsonify(movies_list)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80)
