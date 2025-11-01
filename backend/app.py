"""
app.py
production-minded flask api with user endpoints (list, get, search) backed by mock data
"""

import os
import logging
from typing import List
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from dotenv import load_dotenv

# import data access functions from the mock users module
from data.users import get_all_users, search_user_by_id


def get_allowed_origins(raw: str) -> List[str]:
    """
    parse a comma-separated origins string from env into a clean list.

    params:
        raw (str): the raw env string from CORS_ORIGINS 
    returns:
        List[str]: cleaned list of origins to make it in the proper format
    """
    return [o.strip() for o in (raw or "").split(",") if o.strip()]


def is_valid_id(candidate: str) -> bool:
    """
    validate if the candidate is a valid user id (numeric string).

    params:
        candidate (str): the string to validate
    returns:
        bool: True if candidate is a numeric id, else False
    """
    return candidate.strip().isdigit() if candidate else False


def register_error_handlers(app: Flask) -> None:
    """
    register json error handlers for common http errors

    params:
        app (Flask): the flask app instance
    returns:
        None
    """
    @app.errorhandler(400)
    def handle_400(err):
        return jsonify({"error": {"code": 400, "message": "bad request"}}), 400

    @app.errorhandler(404)
    def handle_404(err):
        return jsonify({"error": {"code": 404, "message": "not found"}}), 404

    @app.errorhandler(500)
    def handle_500(err):
        # do not leak internal server details in production
        return jsonify({"error": {"code": 500, "message": "internal server error"}}), 500


def add_security_headers(app: Flask) -> None:
    """
    attach minimal security headers to every response.

    params:
        app (Flask): the flask app instance
    returns:
        None
    """
    @app.after_request
    def set_headers(resp: Response):
        #no sniff prevents browsers from guessing content types, which help defending against browser-ignoring-types kinds of attacks
        resp.headers["X-Content-Type-Options"] = "nosniff"
        #prevents the site from being embedded in iframes, which stops clickjacking attacks 
        resp.headers["X-Frame-Options"] = "DENY"
        return resp



def create_app() -> Flask:
    """
    build and configure the flask application.

    returns:
        Flask: a configured flask app instance
    """
    # load env vars from .env if present 
    load_dotenv()

    # set up basic console logging, errors will go to stderr
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    logger = logging.getLogger(__name__)

    app = Flask(__name__)

    # set up strict cors using a whitelist from env (no wildcard)
    origins = get_allowed_origins(os.getenv("CORS_ORIGINS", ""))
    CORS(
        app,
        origins=origins,
        supports_credentials=True,
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    )

    # cross-cutting concerns
    register_error_handlers(app)
    add_security_headers(app)

    # -------------------------------------------------------------------------
    # healthcheck (useful for k8s/app runner/etc.)
    # -------------------------------------------------------------------------
    @app.get("/health")
    def health():
        """
        lightweight health check endpoint.
        """
        return jsonify({"status": "ok"}), 200

    # -------------------------------------------------------------------------
    # api: list users
    # -------------------------------------------------------------------------
    @app.get("/api/users")
    def api_list_users():
        """
        get all users (email excluded by the data layer).
        returns:
            200 json: {"users": [...], "total": n}
            500 json on server error
        """
        try:
            users = get_all_users()
            return jsonify({"users": users, "total": len(users)}), 200
        except Exception as exc:  # log and fall back to 500
            logger.exception("failed to list users: %s", exc)
            return jsonify({"error": "internal server error"}), 500

    # -------------------------------------------------------------------------
    # api: get user by id
    # -------------------------------------------------------------------------
    @app.get("/api/users/<user_id>")
    def api_get_user(user_id: str):
        """
        get a single user by id.
        returns:
            200 json: {"user": {...}}
            400 json if id format is invalid
            404 json if user not found
            500 json on server error
        """
        try:
            if not is_valid_id(user_id):
                return jsonify({"error": "invalid user id format"}), 400

            user = get_user_by_id(user_id)
            if user is None:
                return jsonify({"error": "user not found"}), 404

            return jsonify({"user": user}), 200
        except Exception as exc:
            logger.exception("failed to get user %s: %s", user_id, exc)
            return jsonify({"error": "internal server error"}), 500

    # -------------------------------------------------------------------------
    # api: search user by id via query param
    # -------------------------------------------------------------------------
    @app.get("/api/users/search")
    def api_search_user():
        """
        search a user by id passed as a query param `id`.
        returns:
            200 json: {"user": {...}} or {"user": null}
            400 json if id param missing or invalid
            500 json on server error
        """
        try:
            user_id = request.args.get("id", "").strip()
            if not user_id:
                return jsonify({"error": "missing 'id' query parameter"}), 400

            if not is_valid_id(user_id):
                return jsonify({"error": "invalid user id format"}), 400

            user = search_user_by_id(user_id)
            # as required: return user or null (json null) if not found
            return jsonify({"user": user if user is not None else None}), 200
        except Exception as exc:
            logger.exception("failed to search user: %s", exc)
            return jsonify({"error": "internal server error"}), 500

    return app


# create the app instance for wsgi servers (e.g., gunicorn)
app = create_app()


if __name__ == "__main__":
    # local/dev run; in production, prefer:
    # gunicorn -w 4 -b 0.0.0.0:${PORT:-8000} app:app
    port_str = os.getenv("PORT", "8000")
    try:
        port = int(port_str)
    except ValueError:
        port = 8000

    app.run(host="0.0.0.0", port=port)
