from flask import Blueprint, request
import jsonpickle

from repos import user_repo

user_route = Blueprint("user_route", __name__)


@user_route.route("/user/<userId>", methods=["GET"])
def get_user(userId: str):
    try:
        user = user_repo.get_user_by_id(userId)

        return jsonpickle.encode(user)
    except Exception as e:
        return (
            jsonpickle.encode(
                {"error": "Unable to retrieve user by id", "details": str(e)}
            ),
            500,
        )


@user_route.route("/users", methods=["GET"])
def get_all_users():
    try:
        users = user_repo.get_users()
        return jsonpickle.encode(users), 200

    except Exception as e:
        return jsonpickle.encode({"error": "Invalid JSON data", "details": str(e)}), 500


@user_route.route("/user", methods=["POST"])
def create_user():
    try:
        userDetails = request.get_json()

        if userDetails:
            createdUser = user_repo.create_user(userDetails)
            return jsonpickle.encode(createdUser), 200
        else:
            return (
                jsonpickle.encode(
                    {"error": "No JSON data provided in the request body"}
                ),
                422,
            )

    except Exception as e:
        return (
            jsonpickle.encode({"error": "Unable to create user", "details": str(e)}),
            500,
        )


@user_route.route("/user", methods=["PATCH"])
def update_user():
    try:
        updateDetails = request.get_json()

        if updateDetails:
            updatedUser = user_repo.update_user(updateDetails)
            return jsonpickle.encode(updatedUser), 200
        else:
            return (
                jsonpickle.encode(
                    {"error": "No JSON data provided in the request body"}
                ),
                422,
            )

    except Exception as e:
        return (
            jsonpickle.encode({"error": "Unable to update user", "details": str(e)}),
            500,
        )


@user_route.route("/user/<userId>", methods=["DELETE"])
def delete_user(userId):
    try:
        if userId:
            user_repo.delete_user(userId)
            return "success", 200
        else:
            return jsonpickle.encode({"error": "No id provided in the request"}), 422

    except Exception as e:
        return (
            jsonpickle.encode({"error": "Unable to delete user", "details": str(e)}),
            500,
        )
