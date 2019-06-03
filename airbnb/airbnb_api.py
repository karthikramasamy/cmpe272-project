from flask import request, jsonify, Blueprint, _request_ctx_stack, make_response
from airbnb import airbnb_data
from airbnb.airbnb_db import get_db
from airbnb.core import requires_auth
from airbnb.core import jsonify_error

bp = Blueprint('airbnb_api', __name__, url_prefix='/api/v1/')

@bp.route("listings", methods=['GET'])
@requires_auth
def get_listings():
    """
       API to get all the listings in the airbnb.
       """
    try:
        listings = airbnb_data.get_listings(get_db())
        return jsonify(listings)
    except Exception as ex:
        print(ex)
        return jsonify_error("Error while retrieving the listings", 500)


@bp.route("listings/<listing_id>", methods=['GET'])
@requires_auth
def get_listing(listing_id):
    """
       API to get the details of a listing.
       """
    try:
        listing = airbnb_data.get_listing_by_id(get_db(), listing_id)
        if listing:
            return jsonify(listing)
        else:
            return jsonify_error("No listing found for the given listing_id", 404)

    except Exception as ex:
        print(ex)
        return jsonify_error("Error while retrieving the listing by listing_id", 500)


@bp.route("reviews/<listing_id>", methods=['GET'])
@requires_auth
def get_reviews(listing_id):
    """
       API to get the reviews of a listing.
       """
    try:
        reviews = airbnb_data.get_reviews_by_listing_id(get_db(), listing_id)
        return jsonify(reviews)
    except Exception as ex:
        print(ex)
        return jsonify_error("Error while retrieving the reviews by listing_id", 500)
