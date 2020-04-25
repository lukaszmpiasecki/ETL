import sqlite3
from sqlite3 import connect
from argparse import ArgumentParser
import time

create_query1 = 'CREATE TABLE IF NOT EXISTS TABELA1(KLUCZ INTEGER PRIMARY KEY AUTOINCREMENT, ID_USER VARCHAR(250), ID_UTW VARCHAR(250),DATA_OD INTEGER, FOREIGN KEY(ID_UTW) REFERENCES TABELA2(ID_UTW))'
create_query2 = 'CREATE TABLE IF NOT EXISTS TABELA2(ID_WYK VARCHAR(250), ID_UTW VARCHAR(250) PRIMARY KEY, ART VARCHAR(250), UTW VARCHAR(250))'
insert_query1 = 'INSERT INTO TABELA1 (ID_USER, ID_UTW, DATA_OD) VALUES(?,?,?)'
insert_query2 = 'INSERT INTO TABELA2 (ID_WYK, ID_UTW, ART, UTW) VALUES(?,?,?,?)'


def main():
    t = time.time()
    parser = ArgumentParser()
    parser.add_argument('--path', dest='path', type=str, required=True)
    args = parser.parse_args()
    with connect(args.path + '/mydb.db') as conn:
        conn.execute(create_query1)
        conn.execute(create_query2)
        db_cursor = conn.cursor()
        print("Trwa operacja na bazie danych...\n")
        with open(args.path + '/triplets_sample_20p.txt', 'r', encoding='ISO-8859-1') as fd1:
            for i in fd1:
                line = i.split("<SEP>")
                db_cursor.execute(insert_query1, line)
        with open(args.path + '/unique_tracks.txt', 'r', encoding='ISO-8859-1') as fd2:
            for i in fd2:
                line = i.split("<SEP>")
                try:
                    db_cursor.execute(insert_query2, line)
                except sqlite3.Error as e:
                    pass    # eliminuje zduplikowane id utworu
        db_cursor.execute(
            'SELECT UTW FROM TABELA2 AS dwa, (SELECT ID_UTW, COUNT(*) FROM TABELA1 GROUP BY ID_UTW ORDER BY COUNT(*) DESC LIMIT 5) AS top5 WHERE dwa.ID_UTW=top5.ID_UTW')
        result = db_cursor.fetchmany(5)
        print("5 najpopularniejszych utworow to: \n")
        for i in result:
            print(i)
        db_cursor.execute(
            'SELECT ART FROM (SELECT ART, COUNT(*) FROM TABELA1 INNER JOIN TABELA2 ON TABELA1.ID_UTW = TABELA2.ID_UTW GROUP BY ART ORDER BY COUNT(*) DESC LIMIT 5)')
        result = db_cursor.fetchmany(1)
        print("Artysta z najwieksza iloscia odsluchan to: \n")
        for i in result:
            print(i)
    print("Czas: %.2f sekund." % (time.time() - t))


if __name__ == "__main__":
    main()
