from fastapi import FastAPI, Response
from bs4 import BeautifulSoup
import re
import psycopg2 # For Postgres
import datetime
import os
from google.cloud import bigquery
import pandas as pd
from google.cloud import bigquery
# import Jinja2
import random
#from model import get_students_from_course

app = FastAPI()

service_account_json = './backend/udp-mhacks23-03.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = service_account_json
bqclient = bigquery.Client() 

def run_query(bqclient: bigquery.Client, sql: str) -> pd.DataFrame:
    return bqclient.query(sql).result().to_dataframe()

def get_students_from_course(bqclient: bigquery.Client, udp_course_offering_id: int, term: str) -> pd.DataFrame:
    df = run_query(
        bqclient,
        f"SELECT udp_person_id, num_sessions_10min, total_time_seconds_10min, num_sessions_20min, total_time_seconds_20min, num_sessions_30min, total_time_seconds_30min " \
        f"FROM udp-mhacks-november-2023.mart_course_offering.interaction_sessions " \
        f"WHERE role = 'Student' " \
        f"AND udp_course_offering_id = {udp_course_offering_id} " \
        f"AND academic_term_name = '{term}' "
    ).groupby("udp_person_id").sum()
    df["avg_time_sessions_10min"] = df["total_time_seconds_10min"] / df["num_sessions_10min"]
    df["avg_time_sessions_20min"] = df["total_time_seconds_20min"] / df["num_sessions_20min"]
    df["avg_time_sessions_30min"] = df["total_time_seconds_30min"] / df["num_sessions_30min"]
    df = df.drop(columns=["num_sessions_10min", "total_time_seconds_10min", "num_sessions_20min", "total_time_seconds_20min", "num_sessions_30min", "total_time_seconds_30min"])
    return df



# TODO: put list of teachers into our database

def get_grades(course: int):
    """ Query database to get student's grades. """

    course = 279

    # (1) Query1: Get list of students
    sql_query = f'select A.udp_person_id ' + \
                f'from udp-mhacks-november-2023.mart_taskforce.level1_aggregated A, udp-mhacks-november-2023.mart_taskforce.course_profile B ' + \
                f'where A.udp_course_offering_id = B.course_offering_id AND B.course_offering_id = {course}'
    query_job = bqclient.query(sql_query)
    query_results = query_job.result()
    df = query_results.to_dataframe()
    print(df)

    # (2) Query1: Get grades for each student

    # (3) Compute mean and sample deviation

    # (4) Query2: Get interactions for each student

    # TODO: Fake data to test fron end

    context = {"grades": make_prediction(course)}
    return context

#get_grades(1)

def get_interactions(course: int):
    dummy_interaction_data = get_students_from_course(bqclient, course, "Fall 2022")["avg_time_sessions_10min"].to_dict()
    
    return {"interaction": dummy_interaction_data}

#print(get_interactions(10681))

def make_prediction(course):
    """ Evan and Dennis will do this. """
    sql_query = f'select A.udp_person_id ' + \
                f'from udp-mhacks-november-2023.mart_taskforce.level1_aggregated A, udp-mhacks-november-2023.mart_taskforce.course_profile B ' + \
                f'where A.udp_course_offering_id = B.course_offering_id AND B.course_offering_id = {course}'
    query_job = bqclient.query(sql_query)
    query_results = query_job.result()
    df = query_results.to_dataframe()
    output = []
    for i, row in df.iterrows():
        output.append(random.randint(0, 100)) 
    return output

def get_teachers():
    """ Returns list of teachers. """

    # (1) Query1: Get list of teachers
    sql_query = 'SELECT instructor_name_array AS teachers FROM udp-mhacks-november-2023.mart_taskforce.course_profile LIMIT 10'

    query_job = bqclient.query(sql_query)
    query_results = query_job.result()
    teachers = query_results.to_dataframe()

    result = []

    for index, row in teachers.iterrows():

        for teacher in row['teachers']:
            if teacher not in result:
                result.append(teacher)

    result.sort()
    return {"teachers": result}

#print(get_teachers())


def get_classes(first: str, last: str):
    """ Returns all classes taught by the specified teacher. """

    teacher = last + ", " + first

    # (1) Query1: Get list of classes
    sql_query = 'SELECT course_offering_id AS id, course_title ' + \
                'FROM udp-mhacks-november-2023.mart_taskforce.course_profile ' + \
                f'WHERE \'{teacher}\' IN UNNEST(instructor_name_array)'

    # (2) Return result
    query_job = bqclient.query(sql_query)
    query_results = query_job.result()
    courses = query_results.to_dataframe()
    
    res = {}
    for index, row in courses.iterrows():
        id = row['id']
        title = row['course_title']

        res[id] = title

    return res

get_classes("Macy", "Cooper")



@app.get("/api/{course}")
async def root(course: int):
    """ Returns a full roster of students, their predicted grade, and predicted engagement given a course ID. """

    """
    Outputs a dict

        {
            student1: {grade: "", engagement: ""},
            student2: {grade: "", engagement: ""},
            student3: {grade: "", engagement: ""},
        }

    """
    
    return None 

@app.get("/api/teachers/")
async def teachers_endpoint():
    
    """ Returns all teachers. """

    """
    Outputs a dict

        {
            teachers: [name1, name2, name3, ...]
        }

    """
    
    return get_teachers() 

@app.get("/api/classes/{first}/{last}/")
async def classes_endpoint(first, last):
    """ Get the classes taught by a teacher."""
    return get_classes(first, last)

@app.get("/api/grades/{course}/")
async def grades_endpoint(course):
    return get_grades(course)

@app.get("/api/interactions/{course}/")
async def interactions_endpoint(course):
    return get_interactions(course)