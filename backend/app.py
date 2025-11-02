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
from data.users import get_all_users, get_user_by_id


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
    origins = get_allowed_origins(os.getenv("CORS_ORIGINS", "")) #gets the fe's port
    CORS(
        app,
        origins=origins, #whitelists only the fe
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    )

   
    register_error_handlers(app) #catches any error thrown by endpoint
    add_security_headers(app) #add a asecurity header when any response is sent

  
    @app.get("/health")
    def health():
        """
        health check endpoint.
        """
        return jsonify({"status": "ok"}), 200

    
    @app.get("/api/users")
    def api_list_users():
        """
        get all users 
        returns:
            200 json: {"users": [...], "total": n}
            500 json on int-server error
        """
        try:
            users = get_all_users()
            return jsonify({"users": users, "total": len(users)}), 200
        except Exception as exc:  # log and fall back to 500
            logger.exception("failed to list users: %s", exc)
            return jsonify({"error": "internal server error"}), 500

    
    
    @app.get("/api/users/<user_id>")
    def api_get_user(user_id):
        """
        get a single user by id (path param).
        returns:
            200 json: {"user": {...}} if found
            400 json if id invalid
            404 json if not found
            500 json on server error
        """
        try:
            if not is_valid_id(user_id):
                return jsonify({"error": "invalid user id format"}), 400
            user = get_user_by_id(user_id)
            if user is None:
                return jsonify({"error": "not found"}), 404
            return jsonify({"user": user}), 200
        except Exception as exc:
            logger.exception("failed to get user: %s", exc)
            return jsonify({"error": "internal server error"}), 500


    return app


# create the app instance for wsgi server (guni)
app = create_app()


if __name__ == "__main__":
    port_str = os.getenv("PORT", "8000")
    try:
        port = int(port_str)
    except ValueError:
        port = 8000

    app.run(host="0.0.0.0", port=port)
