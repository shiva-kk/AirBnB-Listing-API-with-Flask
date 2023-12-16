import unittest
import json
from app import app

class TestCreateListingEndpoint(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        # Add any setup steps if needed

    def test_create_listing_success(self):
        new_listing_data = {
            "name": "New Listing",
            "host_id": 123,
            "neighbourhood": 78701,
            "room_type": "Entire home/apt",
            "price": 150
        }

        response = self.app.post('/listings', json=new_listing_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], new_listing_data['name'])
        # Add more assertions as needed

    def test_create_listing_bad_request(self):
        invalid_listing_data = "test"

        response = self.app.post('/listings', json=invalid_listing_data)
        self.assertEqual(response.status_code, 400)#201
        self.assertIn('error', response.json)

if __name__ == '__main__':
    unittest.main()
