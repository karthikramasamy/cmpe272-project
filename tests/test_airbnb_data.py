import unittest
import mongomock
import json
import datetime
from airbnb import airbnb_data


class AirbnbUnitTests(unittest.TestCase):

    def setUp(self):
        self.db = mongomock.MongoClient()['airbnb']

    def test_get_listings_count(self):
        count = airbnb_data.get_listings_count(self.db)
        self.assertEqual(count, 22895)
    
    def test_get_listings(self):
        listings = airbnb_data.get_listings(self.db)
        self.assertIsNotNone(listings)

    def test_get_listing_by_id(self):
        listing = airbnb_data.get_listing_by_id(self.db, 9835)
        self.assertIsNotNone(listing)
        self.assertEqual(listing['id'], 9835)

    def test_get_listing_by_unknown_id(self):
        listing = airbnb_data.get_listing_by_id(self.db, '1234')
        self.assertIsNone(listing)


if __name__ == '__main__':
    unittest.main()
