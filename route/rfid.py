from flask import Blueprint, request
import jsonpickle
from app import rfidRepo

rfid_route = Blueprint("rfid_route", __name__)


@rfid_route.route("/rfid/<rfidValue>", methods=["GET"])
def get_rfid(rfidValue: str):
    try:
        rfid = rfidRepo.get_rfid_by_value(rfidValue)

        return jsonpickle.encode(rfid)
    except Exception as e:
        return (
            jsonpickle.encode(
                {"error": "Unable to retrieve rfid by value", "details": str(e)}
            ),
            500,
        )


@rfid_route.route("/rfids", methods=["GET"])
def get_all_rfids():
    try:
        rfids = rfidRepo.get_rfids()
        return jsonpickle.encode(rfids), 200

    except Exception as e:
        return jsonpickle.encode({"error": "Invalid JSON data", "details": str(e)}), 500


@rfid_route.route("/rfid", methods=["POST"])
def create_rfid():
    try:
        rfidDetails = request.get_json()

        if rfidDetails:
            createdRfid = rfidRepo.create_rfid(rfidDetails)
            return jsonpickle.encode(createdRfid), 200
        else:
            return (
                jsonpickle.encode(
                    {"error": "No JSON data provided in the request body"}
                ),
                422,
            )

    except Exception as e:
        return (
            jsonpickle.encode({"error": "Unable to create rfid", "details": str(e)}),
            500,
        )


@rfid_route.route("/rfid", methods=["PATCH"])
def update_rfid():
    try:
        updateDetails = request.get_json()

        if updateDetails:
            updatedRfid = rfidRepo.update_rfid(updateDetails)
            return jsonpickle.encode(updatedRfid), 200
        else:
            return (
                jsonpickle.encode(
                    {"error": "No JSON data provided in the request body"}
                ),
                422,
            )

    except Exception as e:
        return (
            jsonpickle.encode({"error": "Unable to update rfid", "details": str(e)}),
            500,
        )


@rfid_route.route("/rfid/<rId>", methods=["DELETE"])
def delete_rfid(rId):
    try:
        if rId:
            rfidRepo.delete_rfid(rId)
            return "success", 200
        else:
            return jsonpickle.encode({"error": "No id provided in the request"}), 422

    except Exception as e:
        return (
            jsonpickle.encode({"error": "Unable to delete rfid", "details": str(e)}),
            500,
        )
