import os
import logging
import psycopg2
import config as cf
from datetime import datetime

os.environ['DATABASE_URL'] = cf.DATABASE_URL
DATABASE_URL = os.environ['DATABASE_URL']


def create_table():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Creating table as per requirement
    sql = '''CREATE TABLE VISITORENTRY(
    NID SERIAL PRIMARY KEY,
    SENDERID VARCHAR(40) ,
    VISITORNAME VARCHAR(50),
    OTP VARCHAR(4),
    STATUS VARCHAR(1),
    CREATEDDATE TIMESTAMP NOT NULL,
    APPROVEDDATE TIMESTAMP
    );'''
    try:
        cursor.execute(sql)
    except Exception as error:
        print(str(error))

    conn.commit()

    print("Tables created successfully........")

    # Closing the connection
    conn.close()


def insert_data(data):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    query = "INSERT INTO VISITORENTRY(SENDERID, OTP, CREATEDDATE, STATUS)" \
            " VALUES(%s, %s, %s, %s);"

    now = datetime.utcnow()
    TIMESTAMP = now.strftime('%Y-%m-%d %H:%M:%S')

    print(query, (data[0], data[1], TIMESTAMP))
    cursor.execute(query, (data[0], data[1], TIMESTAMP, data[2]))
    conn.commit()
    print("Data inserted successfully........")

    # Closing the connection
    conn.close()


def update_data(data):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    query = "UPDATE VISITORENTRY SET VISITORNAME = %s, STATUS = %s " \
            "WHERE SENDERID = %s AND OTP = %s;"
    print(query.format(), data[0], data[1], data[2], data[3])

    cursor.execute(query, (data[0], data[1], data[2], data[3]))
    conn.commit()
    print("Data inserted successfully........")

    # Closing the connection
    conn.close()


def get_otp(data):
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        query = "SELECT SENDERID FROM VISITORENTRY WHERE OTP = %s AND STATUS = %s"

        cur.execute(query, (data[0], data[1]))

        result = []
        row = cur.fetchone()
        if row is None:
            return []

        while row is not None:
            result.append(row[0])
            row = cur.fetchone()
            if row is None:
                break
            result.append(row[0])

        cur.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def get_data(data):
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        query = "SELECT VISITORNAME, OTP FROM VISITORENTRY WHERE SENDERID = %s AND STATUS = %s"

        cur.execute(query, (data[0], data[1]))

        result = []
        row = cur.fetchone()
        if row is None:
            return []

        while row is not None:
            result.append((row[0], row[1]))
            row = cur.fetchone()
            if row is None:
                break
            result.append((row[0], row[1]))

        cur.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def delete_user_data(psid):
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        query = "DELETE FROM USERINTENT WHERE PSID = %s;"
        cur.execute(query, (psid,))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    #create_table()
    #insert_data(data=["31232132131", "0234", "0])
    update_data(data=["M", "0", "3125061030937118", "5478"])
    #print(get_data(data=["31232132131", "0"]))
    #print(get_otp(data=["6808", "0"]))
    print("inr")