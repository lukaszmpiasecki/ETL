import sqlite3
from sqlite3 import connect
from argparse import ArgumentParser
import csv

create_query = 'CREATE TABLE IF NOT EXISTS TABELA(ID_WYK VARCHAR(250) PRIMARY KEY, ID_UTW VARCHAR(250), ART VARCHAR(' \
               '250), UTW VARCHAR(250)) '
insert_query = 'INSERT INTO TABELA (ID_WYK, ID_UTW, ART, UTW) VALUES(?,?,?,?)'


def main():
    with connect('database.db') as conn:
        conn.execute(create_query)
        db_cursor = conn.cursor()
        with open('/home/student/Pobrane/unique_tracks.txt', 'r', encoding='ISO-8859-1') as fd:
            for i in fd:
                line = i.split("<SEP>")
                db_cursor.execute(insert_query, line)


if __name__ == "__main__":
    main()
