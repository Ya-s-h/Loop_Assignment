from rq import Queue
from worker import conn
# import uuid
from datetime import datetime, timezone
from libs import calculate_store_time, calculating_time_for_each_store
import flask
import json
blueprint = flask.Blueprint("report_api", __name__, url_prefix="/api/v1")

futures_dict = {}
# executor = ProcessPoolExecutor(max_workers=None)
server_time = datetime(2023, 1, 25, 0, 56, 23, tzinfo=timezone.utc)
q = Queue(connection=conn)

@blueprint.route("/trigger_report", methods=['POST'])
def trigger_report():
    store_id = flask.request.get_json()['store_id']
    job = q.enqueue(calculate_store_time, store_id)
    job_id = job.get_id()
    return flask.jsonify({"status": 200, "job_id": job_id})
# def trigger_report():
#
#     res_hour, res_day, res_week= calculate_store_time(server_time,flask.request.get_json()['store_id'] )
#
#     results= {
#         "store_id": flask.request.get_json()['store_id'],
#         "uptime_in_last_hour (minutes)": res_hour[1].total_seconds()/ 60,
#         "uptime_in_last_day (hours)": res_day[1].total_seconds() / 3600,
#         "uptime_in_last_week (hours)": res_week[1] / 3600,
#         "downtime_in_last_hour (minutes)": res_hour[0].total_seconds() / 60,
#         "downtime_in_last_day (hours)": res_day[0].total_seconds() / 3600,
#         "downtime_in_last_week (hours)": res_week[0] / 3600,
#
#     }
#     return flask.jsonify({"status": 200, "results": results})
#

@blueprint.route("/get_report/<job_id>", methods=["GET"])
def get_report(job_id):
    job = q.fetch_job(job_id)
    print(job)
    if job is not None and job.is_finished:
        res_hour, res_day, res_week = job.result
        results = {
            "store_id": job.args[0],
            "uptime_in_last_hour (minutes)": res_hour.total_seconds() / 60,
            "uptime_in_last_day (hours)": res_day.total_seconds() / 3600,
            "uptime_in_last_week (hours)": res_week.total_seconds() / 3600,
            "downtime_in_last_hour (minutes)": (res_hour - timedelta(minutes=30)).total_seconds() / 60,
            "downtime_in_last_day (hours)": (res_day - timedelta(hours=8)).total_seconds() / 3600,
            "downtime_in_last_week (hours)": (res_week - timedelta(hours=40)).total_seconds() / 3600,
        }
        return flask.jsonify({"status": 200, "results": results})
    elif job is not None and job.is_queued:
        return flask.jsonify({"status": 202, "message": "Task in progress"})
    else:
        return flask.jsonify({"status": 404, "message": "Task not found"})