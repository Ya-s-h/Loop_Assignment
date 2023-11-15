from rq import Queue
from worker import conn
# import uuid
from datetime import datetime, timezone
from libs import calculate_store_time
import flask
import json
blueprint = flask.Blueprint("report_api", __name__, url_prefix="/api/v1")

futures_dict = {}
# executor = ProcessPoolExecutor(max_workers=None)
server_time = datetime(2023, 1, 25, 0, 56, 23, tzinfo=timezone.utc)
q = Queue(connection=conn)

@blueprint.route("/trigger_report", methods=['POST'])
def trigger_report():
    """
          Triggers the generation of a report for a specific store based on the provided data.
          Expects a JSON payload in the POST request containing the store_id.
          Returns:
              flask.Response: A JSON response containing the status and results of the triggered report.
              """
    res_hour, res_day, res_week= calculate_store_time(server_time,flask.request.get_json()['store_id'] )

    results= {
        "store_id": flask.request.get_json()['store_id'],
        "uptime_in_last_hour (minutes)": res_hour[1].total_seconds()/ 60,
        "uptime_in_last_day (hours)": res_day[1].total_seconds() / 3600,
        "uptime_in_last_week (hours)": res_week[1] / 3600,
        "downtime_in_last_hour (minutes)": res_hour[0].total_seconds() / 60,
        "downtime_in_last_day (hours)": res_day[0].total_seconds() / 3600,
        "downtime_in_last_week (hours)": res_week[0] / 3600,

    }
    return flask.jsonify({"status": 200, "results": results})

# This function was intended for handling report retrieval but is currently causing performance issues
# Keeping it as a reference and indicating its purpose
"""
@blueprint.route("/get_report", methods=["GET"])
def get_report():
    global futures_dict

    # Get report_id from the request query parameters

    report_id =  flask.request.get_json()['report_id']

    print(f"In get_report\nReport ID={report_id}")
    # Check if the report_id exists in futures_dict
    if report_id in futures_dict:
        result = futures_dict[report_id]
        return  result
        # all_completed = result.done()
        # print(result)
        # if all_completed:
        #     # All tasks are completed, send the result
        #     # result = result_dict.result()
        #     return result.result()
        # else:
        #     # Some tasks are still running, send a response as running
        #     return flask.jsonify({"status": "Running", "message": "Report is still being processed"})
    else:
        return flask.jsonify({"status": "Error", "message": "Report ID not found"})
"""