import concurrent.futures
import uuid
from datetime import datetime, timezone
from libs import calculate_store_time
import flask
import json
blueprint = flask.Blueprint("report_api", __name__, url_prefix="/api/v1")

futures_dict = {}
executor = concurrent.futures.ThreadPoolExecutor()
server_time = datetime(2023, 1, 25, 0, 56, 23, tzinfo=timezone.utc)

@blueprint.route("/trigger_report", methods=['POST'])
def trigger_report():
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
