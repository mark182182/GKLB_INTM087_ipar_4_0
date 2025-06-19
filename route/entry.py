import logging
from flask import Blueprint
import jsonpickle
from repos import entry_repo

entry_route = Blueprint("entry_route", __name__)

logger = logging.getLogger(__name__)


@entry_route.route("/entry/user/<userId>", methods=["GET"])
def get_entry_by_user(userId: str):
    try:
        userEntry = entry_repo.get_entry_by_user(userId)

        return jsonpickle.encode(userEntry)
    except Exception as e:
        logger.error(f"Error retrieving entry for user {userId}: {e}")
        return (
            jsonpickle.encode(
                {"error": "Unable to retrieve entry for user", "details": str(e)}
            ),
            500,
        )


@entry_route.route("/entry", methods=["GET"])
def get_entries_for_all_users():
    try:
        userEntries = entry_repo.get_entries_for_all_users()

        return jsonpickle.encode(userEntries)
    except Exception as e:
        logger.error(f"Error retrieving entries for all users: {e}")
        return (
            jsonpickle.encode(
                {"error": "Unable to retrieve entries for all users", "details": str(e)}
            ),
            500,
        )


@entry_route.route("/entry/rfid/<rfidValue>", methods=["GET"])
def check_entry_for_rfid(rfidValue: str):
    try:
        logger.info(f"Checking entry for RFID: {rfidValue}")
        userEntry = entry_repo.check_entry_for_rfid(rfidValue)
        return jsonpickle.encode(userEntry), 200
    except Exception as e:
        logger.error(f"Error checking entry for RFID {rfidValue}: {e}")
        return (
            jsonpickle.encode(
                {"error": "Unable to enter using rfid", "details": str(e)}
            ),
            500,
        )
