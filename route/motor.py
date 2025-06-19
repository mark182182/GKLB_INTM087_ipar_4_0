from flask import Blueprint, request
import jsonpickle
from models.motor import MotorThreshold
from services import motor_service
from repos import motor_event_repo

import logging

logger = logging.getLogger(__name__)


motor_route = Blueprint("motor_route", __name__)


@motor_route.route("/motor/config", methods=["GET"])
def get_thresholds():
    try:
        return jsonpickle.encode(motor_service.get_threshold())
    except Exception as e:
        logger.error(f"Error retrieving motor thresholds: {e}")
        return jsonpickle.encode({"error": "Failed to retrieve motor thresholds"}), 500


@motor_route.route("/motor/config", methods=["PUT"])
def set_thresholds():
    try:
        data = request.get_json()
        speed_pct = data.get("speed_pct")
        critical_temp = data.get("critical_temp")
        motor_service.set_threshold(MotorThreshold(speed_pct, critical_temp))
        return jsonpickle.encode({"status": "ok"})
    except Exception as e:
        logger.error(f"Error setting motor thresholds: {e}")
        return (
            jsonpickle.encode(
                {"error": "Failed to set motor thresholds", "details": str(e)}
            ),
            500,
        )


@motor_route.route("/motor_event", methods=["GET"])
def get_events():
    try:
        userId = request.args.get("userId")
        logger.info(f"Retrieving motor events for userId: {userId}")
        events = motor_event_repo.get_events(userId)
        return jsonpickle.encode([e.__dict__ for e in events]), 200
    except Exception as e:
        logger.error(f"Error retrieving motor events: {e}")
        return (
            jsonpickle.encode(
                {"error": "Failed to retrieve motor events", "details": str(e)}
            ),
            500,
        )
