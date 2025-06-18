from flask import Blueprint, request
import jsonpickle

from app import userIdRepo

user_id_route = Blueprint("user_id_route", __name__)


@user_id_route.route("/userIdentifier/<userId>", methods=["GET"])
def get_user_identifier_by_user(userId: str):
    try:
        user = userIdRepo.get_user_identifier_by_user(userId)

        return jsonpickle.encode(user)
    except Exception as e:
        return (
            jsonpickle.encode(
                {
                    "error": "Unable to retrieve userIdentifier for user",
                    "details": str(e),
                }
            ),
            500,
        )


@user_id_route.route("/userIdentifier", methods=["POST"])
def add_rfid_to_user():
    try:
        userIdentifierDetails = request.get_json()
        userIdentifier = userIdRepo.add_rfid_to_user(userIdentifierDetails)

        return jsonpickle.encode(userIdentifier)
    except Exception as e:
        return (
            jsonpickle.encode(
                {"error": "Unable to add rfid to user", "details": str(e)}
            ),
            500,
        )


@user_id_route.route("/userIdentifier/disabled/<isDisabled>", methods=["PATCH"])
def update_disabled_for_user_identifier(isDisabled: bool):
    try:
        userIdentifierDetails = request.get_json()
        userIdentifierDetails["disabled"] = int(isDisabled)
        userIdentifier = userIdRepo.update_disabled_for_user_identifier(
            userIdentifierDetails
        )

        return jsonpickle.encode(userIdentifier)
    except Exception as e:
        return (
            jsonpickle.encode(
                {
                    "error": "Unable to change disabled state for userIdentifier",
                    "details": str(e),
                }
            ),
            500,
        )


@user_id_route.route("/userIdentifier/<rfidValue>", methods=["DELETE"])
def remove_rfid_from_user(rfidValue: str):
    try:
        userIdRepo.remove_rfid_from_user(rfidValue)

        return "success", 200
    except Exception as e:
        return (
            jsonpickle.encode(
                {"error": "Unable to add rfid to user", "details": str(e)}
            ),
            500,
        )
