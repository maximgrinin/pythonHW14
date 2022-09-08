import sqlite3

# Определяем переменную с именем БД
DATA_BASE = 'netflix.db'


# Функция возвращает фильмы по заданным в параметрах Типу, Году и Жанру
def get_by_args(movie_type='Movie', year=2010, genre='Dramas'):
    with sqlite3.connect(DATA_BASE) as connection:
        cursor = connection.cursor()
        query = f"""
                select nf.title, nf.description
                from netflix nf
                where nf.type = '{movie_type}'\
                  and nf.release_year = {year}
                  and nf.listed_in like '%{genre}%'
                order by nf.release_year desc, nf.date_added desc
        """
        cursor.execute(query)
        movies_list = [dict((cursor.description[i][0], value)
                       for i, value in enumerate(row)) for row in cursor.fetchall()]

        print(movies_list)

        return 0


# Функция для задания 5 со множествами
def task_5(actor_1, actor_2):
    actors_all = []

    with sqlite3.connect(DATA_BASE) as connection:
        cursor = connection.cursor()
        query = f"""
                select nf.cast
                from netflix nf
                where nf.cast != '' and nf.cast is not null
                  and nf.cast like '%{actor_1}%'
                  and nf.cast like '%{actor_2}%'
                group by nf.cast
        """
        cursor.execute(query)
        result = cursor.fetchall()

        # Собираем полный список всех актеров
        for movie in result:
            actors = movie[0].split(", ")
            actors_all.extend(actors)

        # Оставляем тех, кто встречается дважды
        actors_seen_twice = {actor for actor in actors_all if actors_all.count(actor) > 2} - {actor_1, actor_2}
        print(actors_seen_twice)

        return 0


if __name__ == "__main__":
    get_by_args()
    task_5('Jack Black', 'Dustin Hoffman')
    task_5('Rose McIver', 'Ben Lamb')
