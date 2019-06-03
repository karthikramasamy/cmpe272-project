def get_listings_count(db):
    return db.listings.count_documents({})


def get_listings(db):
    return list(db.listings.find({}, {'id': 1, 'name': 1, 'city': 1, 'state': 1, 'zipcode': 1, 'price': 1, 'room_type': 1, 'host_name': 1}))


def get_listing_by_id(db, listing_id):
    return db.listings.find_one({'_id': int(listing_id)})


def get_reviews_by_listing_id(db, listing_id):
    return list(db.reviews.find({'listing_id': int(listing_id)}))


if __name__ == "__main__":

    from airbnb import create_app
    from airbnb import airbnb_db

    app = create_app()

    with app.app_context():
        db = airbnb_db.init_db()

        print("\n Count of all listings: ", get_listings_count(db))
        print("\n Listing Details for listing id 9835: \n")
        print(get_listing_by_id(db, 9835))
        print("\n Reviews for listing id 9835: \n")
        for review in get_reviews_by_listing_id(db, 9835):
            print(review)
