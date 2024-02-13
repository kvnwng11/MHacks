import os

from google.cloud import bigquery
import pandas as pd

service_account_json = './backend/udp-mhacks23-03.json'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_json
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

print(get_students_from_course(bqclient, 10681, "Fall 2022"))