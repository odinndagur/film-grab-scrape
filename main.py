import selenium
from selenium import webdriver
import time

import sqlite3
import os

db_path = 'film-grab-db.sqlite3'
# os.remove(db_path)
os.rename(db_path, f'backup-{db_path}')

def init_db(db):
    stmts = [
        'CREATE TABLE movie(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT,year INTEGER,director_id INTEGER,dop_id INTEGER,production_designer_id INTEGER,costume_designer_id INTEGER,filmgrab_url TEXT);',
        'CREATE TABLE director(id INTEGER PRIMARY KEY AUTOINCREMENT,name);',
        'CREATE TABLE director_of_photography(id INTEGER PRIMARY KEY AUTOINCREMENT,name)',
        'CREATE TABLE production_designer(id INTEGER PRIMARY KEY AUTOINCREMENT,name);',
        'CREATE TABLE costume_designer(id INTEGER PRIMARY KEY AUTOINCREMENT,name);',
        'CREATE TABLE movie_image(movie_id,image_url);'
    ]
    for s in stmts:
        print(s)
        db.execute(s)
    

with sqlite3.connect(db_path) as db:
    init_db(db)
    # quit()
    # print(db.execute('select * from sqlite_master').fetchall())
    # quit()

    driver = webdriver.Safari(keep_alive=False)
    # driver.implicitly_wait(20)
    # driver.set_page_load_timeout(30)
    base_url = 'https://film-grab.com/movies-a-z/'

    driver.get(base_url)
    movies = driver.find_elements_by_class_name('listing-item')
    for movie in movies:
        title = movie.text
        link = movie.find_element_by_class_name('title')

        filmgrab_url = link.get_attribute('href')
        print(f'{title=} {filmgrab_url=}')
        link.click()
        time.sleep(5)

        p_elements = driver.find_elements_by_tag_name('p')
        for el in p_elements:
            if 'Director: ' in el.text:
                director = el.text.split('Director: ')[1]
                print(el.text)
            if 'Director of Photography: ' in el.text:
                director_of_photography = el.text.split('Director of Photography: ')[1]
                print(el.text)
            if 'Production Design: ' in el.text:
                production_designer = el.text.split('Production Design: ')[1]
                print(el.text)
            if 'Costume Design: ' in el.text:
                costume_designer = el.text.split('Costume Design: ')[1]
                print(el.text)
            if 'Year: ' in el.text:
                year = el.text.split('Year: ')[1]
                print(el.text)
        time.sleep(5)
        imgs = driver.find_elements_by_class_name('bwg_lightbox')
        img_urls = [img.get_attribute('href') for img in imgs]
        # print(imgs)


        print(f'''
            {title=}
            {filmgrab_url=}
            {director=}
            {director_of_photography=}
            {production_designer=}
            {costume_designer=}
            {year=}
            {img_urls=}
            ''')
        
        if not db.execute('SELECT * FROM director WHERE name = ?',[director]).fetchall():
            db.execute('INSERT INTO director(name) VALUES(?)',[director])
        if not db.execute('SELECT * FROM director_of_photography WHERE name = ?',[director_of_photography]).fetchall():
            db.execute('INSERT INTO director_of_photography(name) VALUES(?)',[director_of_photography])
        if not db.execute('SELECT * FROM costume_designer WHERE name = ?',[costume_designer]).fetchall():
            db.execute('INSERT INTO costume_designer(name) VALUES(?)',[costume_designer])
        if not db.execute('SELECT * FROM production_designer WHERE name = ?',[production_designer]).fetchall():
            db.execute('INSERT INTO production_designer(name) VALUES(?)',[production_designer])
        
        db.execute('''
        INSERT INTO movie(title,year,filmgrab_url,director_id,dop_id,production_designer_id,costume_designer_id)
        SELECT ?,?,?,director.id,dop.id,production_designer.id,costume_designer.id
        FROM director
        LEFT JOIN director_of_photography as dop
        LEFT JOIN production_designer
        LEFT JOIN costume_designer
        WHERE director.name = ?
        AND dop.name = ?
        AND production_designer.name = ?
        AND costume_designer.name = ?
        ''',[title,year,filmgrab_url,director,director_of_photography,production_designer,costume_designer])

        db.executemany('INSERT INTO movie_image(movie_id,image_url) SELECT movie.id, ? from movie where movie.title = ?',[(img_url,title) for img_url in img_urls])
        # 'CREATE TABLE movie_image(movie_id,image_url);'

        driver.back()
        