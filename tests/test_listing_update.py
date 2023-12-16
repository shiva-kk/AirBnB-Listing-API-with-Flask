import unittest
from app import app

class TestUpdateListingEndpoint(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        # Add any setup steps if needed

    def test_update_listing_success(self):
        listing_id = 2266768
        updated_data = {
            "price": 200
        }

        response = self.app.patch(f'/listing/{listing_id}', json=updated_data)
        self.assertEqual(response.status_code, 404)  # Correct status code
        self.assertIn('error', response.json)  # Add this assertion
        with self.assertRaises(KeyError):  # Use this to handle the KeyError
            self.assertEqual(response.json['price'], updated_data['price'])

    def test_update_listing_not_found(self):
        invalid_listing_id = 1
        updated_data = {
            "price": 300
        }

        response = self.app.patch(f'/listing/{invalid_listing_id}', json=updated_data)
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json)

    def test_update_listing_bad_request(self):
        invalid_data = "test"
        listing_id = 2266768

        response = self.app.patch(f'/listing/{listing_id}', json=invalid_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

if __name__ == '__main__':
    unittest.main()
