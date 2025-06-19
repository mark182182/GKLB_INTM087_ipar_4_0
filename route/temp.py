from datetime import datetime
import jsonpickle
from flask import Blueprint, request
from repos import temp_repo

import logging

logger = logging.getLogger(__name__)

temp_route = Blueprint("temp_route", __name__)


@temp_route.route("/temperature", methods=["GET"])
def get_temperatures():
    try:
        start = request.args.get("start")
        end = request.args.get("end")
        logger.info("Retrieving temperatures from %s to %s", start, end)

        temps = temp_repo.get_temperatures(start, end)
        result = []
        for t in temps:
            d = t.__dict__.copy()
            if isinstance(d.get("measured_at"), datetime):
                d["measured_at"] = d["measured_at"].strftime("%Y-%m-%d %H:%M:%S")
            result.append(d)
        return jsonpickle.encode(result), 200

    except Exception as e:
        return {"error": "Failed to retrieve temperatures", "details": str(e)}, 500
