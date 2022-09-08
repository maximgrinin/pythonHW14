import sqlite3

# Определяем переменные с именем БД и набором рейтингов
DATA_BASE = 'netflix.db'
CHILDREN_RATING = 'G'
FAMILY_RATING = ('G', 'PG', 'PG-13')
ADULT_RATING = ('R', 'NC-17')


# Функция возвращает самый свежий фильм по его названию (вхождение в название)
def get_by_title(title):
    with sqlite3.connect(DATA_BASE) as connection:
        cursor = connection.cursor()
        query = f"""
                select title, country, release_year, listed_in as genre, description
                from netflix
                where title like '%{title}%'
                order by release_year desc, date_added desc
                limit 1
        """
        cursor.execute(query)
        movies_list = [dict((cursor.description[i][0], value)
                       for i, value in enumerate(row)) for row in cursor.fetchall()]
        movie = movies_list[0]

        return movie


# Функция возвращает фильмы (максимум 100) за заданный период в годах
def get_by_period(year_start, year_end):
    with sqlite3.connect(DATA_BASE) as connection:
        cursor = connection.cursor()
        query = f"""
                select title, release_year
                from netflix
                where release_year between {year_start} and {year_end}
                order by release_year desc, date_added desc
                limit 100
        """
        cursor.execute(query)
        movies_list = [dict((cursor.description[i][0], value)
                       for i, value in enumerate(row)) for row in cursor.fetchall()]

        return movies_list


# Функция возвращает фильмы (максимум 100) по заданному в параметрах рейтингу (набору рейтингов)
def get_by_rating(rating):
    with sqlite3.connect(DATA_BASE) as connection:
        match rating:
            case 'children':
                rating_list = CHILDREN_RATING
            case 'family':
                rating_list = FAMILY_RATING
            case 'adult':
                rating_list = ADULT_RATING
            case _:
                rating_list = ()

        cursor = connection.cursor()
        query = f"""
                select title, rating, description
                from netflix
                where rating in ({','.join('"%s"'%rating for rating in rating_list)})
                order by release_year desc, date_added desc
                limit 100
        """

        cursor.execute(query)
        movies_list = [dict((cursor.description[i][0], value)
                       for i, value in enumerate(row)) for row in cursor.fetchall()]

        return movies_list


# Функция возвращает фильмы (максимум 10) по заданному жанру (вхождению в список жанров)
def get_by_genre(genre):
    with sqlite3.connect(DATA_BASE) as connection:
        cursor = connection.cursor()
        query = f"""
                select title, description
                from netflix
                where listed_in like '%{genre}%'
                order by release_year desc, date_added desc
                limit 10
        """
        cursor.execute(query)
        movies_list = [dict((cursor.description[i][0], value)
                       for i, value in enumerate(row)) for row in cursor.fetchall()]

        return movies_list
