import app
import jsonpickle
from flask import Blueprint, request
from repo.temp import TemperatureRepo

import logging

logger = logging.getLogger(__name__)

temp_route = Blueprint("temp_route", __name__)


@temp_route.route("/temperature", methods=["GET"])
def get_temperatures():
    try:
        start = request.args.get("start")
        end = request.args.get("end")
        logger.info("Retrieving temperatures from %s to %s", start, end)

        temps = TemperatureRepo.get_temperatures(start, end)
        return jsonpickle.encode([t.__dict__ for t in temps]), 200

    except Exception as e:
        return {"error": "Failed to retrieve temperatures", "details": str(e)}, 500
